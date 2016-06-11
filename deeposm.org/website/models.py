"""Models for deeposm.org."""

class MapError(models.Model):
	"""An error reported by DeepOSM."""
    created_date = models.DateTimeField(auto_now_add=True)
	solved_date = models.DateTimeField()
    ne = models.PointField()
    sw = models.PointField()
	raster_filename = models.CharField()
	raster_tile_x = models.IntegerField()
	raster_tile_y = models.IntegerField()
    flagged_count = models.IntegerField()

   