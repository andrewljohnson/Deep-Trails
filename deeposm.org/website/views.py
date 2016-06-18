"""Views for deeposm.org."""

from django.http import HttpResponse, JsonResponse
from django.template import loader
import boto3
import datetime
import os
import pickle
from website import models, settings

FINDINGS_S3_BUCKET = 'deeposm'

STATE_NAMES_TO_ABBREVS = {
    'delaware': 'de',
    'maine': 'me',
    'new-hampshire': 'nh',  # nh is unused
}


def home(request):
    """The home page for deeposm.org."""
    template = loader.get_template('home.html')
    return HttpResponse(template.render(request))


def view_error(request, analysis_type, country_abbrev, state_name, error_id):
    """View the error with the given error_id."""
    error = models.MapError.objects.get(id=error_id)
    if request.POST:
        error.flagged_count += 1
        error.save()

    context = {
        'center': ((error.ne_lon + error.sw_lon) / 2, (error.ne_lat + error.sw_lat) / 2),
        'error': error,
        'country_abbrev': country_abbrev,
        'state_name': state_name,
        'analysis_title': analysis_type.replace('-', ' ').title(),
        'analysis_type': analysis_type,
    }
    template = loader.get_template('view_error.html')
    return HttpResponse(template.render(context, request))


def list_errors(request, analysis_type, country_abbrev, state_name):
    """List all the errors of a given type in the country/state."""
    cache_findings()
    template = loader.get_template('list_errors.html')
    analysis_title = analysis_type.replace('-', ' ').title()
    if request.GET.get('flagged'):
        analysis_title = 'Flagged ' + analysis_title
        errors = sorted_findings(state_name, flagged_count=1)
    else:
        errors = sorted_findings(state_name)

    context = {
        'country_abbrev': country_abbrev,
        'state_name': state_name,
        'analysis_type': analysis_type,
        'analysis_title': analysis_title,
        'errors': errors,
    }

    if request.GET.get("json"):
        json_errors = []
        for e in errors:
            json_errors.append({'id': e.id,
                                'certainty': e.certainty,
                                'center': ((e.ne_lon + e.sw_lon) / 2, (e.ne_lat + e.sw_lat) / 2)})
        context['errors'] = json_errors
        return JsonResponse(context)

    return HttpResponse(template.render(context, request))


def sorted_findings(state_name, flagged_count=0):
    """Return a list of errors for the path, sorted by probability."""
    return models.MapError.objects.filter(state_abbrev=STATE_NAMES_TO_ABBREVS[state_name],
                                          solved_date=None,
                                          flagged_count__gte=flagged_count).order_by('-certainty')


def cache_findings():
    """Download findings from S3."""
    s3 = boto3.resource('s3')
    deeposm_bucket = s3.Bucket(FINDINGS_S3_BUCKET)
    for obj in deeposm_bucket.objects.all():
        local_path = 'website/static/' + obj.key
        try:
            os.mkdir('website/static/' + obj.key.split('/')[0])
        except:
            pass
        if True or not os.path.exists(local_path):
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_client.download_file(FINDINGS_S3_BUCKET, obj.key, local_path)
            with open(local_path, 'r') as infile:
                errors = pickle.load(infile)

            naip_errors = naip_map_for_errors(errors)

            for e in errors:
                filename = e['raster_filename']
                updated_error = False
                try:
                    map_error = models.MapError.objects.get(raster_filename=filename,
                                                            raster_tile_x=e['raster_tile_x'],
                                                            raster_tile_y=e['raster_tile_y'],
                                                            )
                    updated_error = True
                except:
                    map_error = models.MapError(raster_filename=filename,
                                                raster_tile_x=e['raster_tile_x'],
                                                raster_tile_y=e['raster_tile_y'],
                                                state_abbrev=e['state_abbrev'],
                                                ne_lat=e['ne_lat'],
                                                ne_lon=e['ne_lon'],
                                                sw_lat=e['sw_lat'],
                                                sw_lon=e['sw_lon']
                                                )
                if updated_error:
                    naip_errors[filename].remove(map_error.id)
                    map_error.solved_date = None

                map_error.certainty = e['certainty']
                map_error.save()

            # set any finding that didn't re-occur as solved in DB
            for key in naip_errors:
                fixed_errors = models.MapError.objects.filter(
                    id__in=naip_errors[key])
                for f in fixed_errors:
                    f.solved_date = datetime.date.utcnow()
                    f.save()

            print("DOWNLOADED {}".format(obj.key))
        else:
            print("ALREADY DOWNLOADED {}".format(obj.key))


def naip_map_for_errors(errors):
    """Return a map of NAIP filename to list of error_ids for that NAIP in the DB."""
    naip_errors = {}
    for e in errors:
        filename = e['raster_filename']
        if filename not in naip_errors:
            # keep track of which errors dont exist for the import, to
            # mark as solved
            errors_for_naip = models.MapError.objects.filter(
                raster_filename=filename)
            error_ids = []
            for err in errors_for_naip:
                error_ids.append(err.id)
            naip_errors[filename] = error_ids
    return naip_errors
