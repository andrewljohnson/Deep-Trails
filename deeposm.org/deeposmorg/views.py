from django.http import HttpResponse
from django.template import loader

def home(request):
  	template = loader.get_template('home.html')
  	context = {
        'foo': 'bar',
    }
  	return HttpResponse(template.render(context, request))


def list_errors(request, country_abbrev, state_name, analysis_type):
  	template = loader.get_template('list_errors.html')
  	context = {
        'country_abbrev': country_abbrev,
        'state_name': state_name,
        'analysis_type': analysis_type.replace('-',' ').title(),
    }
  	return HttpResponse(template.render(context, request))