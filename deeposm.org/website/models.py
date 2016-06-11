"""Models for deeposm.org."""

from django.db import models


class MapError(models.Model):
    """An error reported by DeepOSM."""

    created_date = models.DateTimeField(auto_now_add=True)
    solved_date = models.DateTimeField()
    ne_lat = models.FloatField()
    ne_lon = models.FloatField()
    sw_lat = models.FloatField()
    sw_lon = models.FloatField()
    certainty = models.FloatField()
    raster_filename = models.CharField(max_length=512)
    raster_tile_x = models.IntegerField()
    raster_tile_y = models.IntegerField()
    flagged_count = models.IntegerField()
    # US states just have 2, maybe some country has 5 letter abbreviations?
    state_abbrev = models.CharField(max_length=5)
