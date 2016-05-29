from django.http import HttpResponse
from django.template import loader

TEST_ERROR_DICT = {'id':1, 'certainty':.6, 'source_image': 'http://foo/some_naip.tiff', 
               'source_image_x':2, 'source_image_y':3, 'tile_size': 64, 
               'neLat':32, 'neLon': -112, 'swLat': 31, 'swLon': -113 
              }

def home(request):
    """The home page for deeposm.org."""
    template = loader.get_template('home.html')
    return HttpResponse(template.render(request))


def view_error(request, analysis_type, error_id):
    """View the error with the given error_id"""
    template = loader.get_template('view_error.html')
    error = TEST_ERROR_DICT
    context = {
      'error': error,
      'analysis_title': analysis_type.replace('-',' ').title(),
      'analysis_type': analysis_type,
    }
    return HttpResponse(template.render(context, request))


def list_errors(request, analysis_type, country_abbrev, state_name):
    """List all the errors of a given type in the country/state"""
    template = loader.get_template('list_errors.html')
    errors = [TEST_ERROR_DICT]
    context = {
      'country_abbrev': country_abbrev,
      'state_name': state_name,
      'analysis_type': analysis_type,
      'analysis_title': analysis_type.replace('-',' ').title(),
      'errors': errors,
    }    
    return HttpResponse(template.render(context, request))