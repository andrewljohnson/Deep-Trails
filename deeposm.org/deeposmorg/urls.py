"""deeposmorg URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from views import home, list_errors


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^predictions/(?P<country_abbrev>[^/]*)/(?P<state_name>[^/]*)/(?P<analysis_type>[^/]*)/$', list_errors),
    url(r'^', home),
]
