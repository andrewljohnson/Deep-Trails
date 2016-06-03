"""Methods for working with geo/raster data."""

from functools import partial
from osgeo import gdal, osr
from pyproj import Proj, transform

def lat_lon_to_pixel(raster_dataset, location):
    """From zacharybears.com/using-python-to-translate-latlon-locations-to-pixels-on-a-geotiff/."""
    ds = raster_dataset
    gt = ds.GetGeoTransform()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())
    srs_lat_lon = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs_lat_lon, srs)
    new_location = [None, None]
    # Change the point locations into the GeoTransform space
    (new_location[1], new_location[0], holder) = ct.TransformPoint(location[1], location[0])
    # Translate the x and y coordinates into pixel values
    x = (new_location[1] - gt[0]) / gt[1]
    y = (new_location[0] - gt[3]) / gt[5]
    return (int(x), int(y))


def pixel_to_lat_lon(raster_dataset, col, row):
    """From zacharybears.com/using-python-to-translate-latlon-locations-to-pixels-on-a-geotiff/."""
    ds = raster_dataset
    gt = ds.GetGeoTransform()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())
    srs_lat_lon = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs, srs_lat_lon)
    ulon = col * gt[1] + gt[0]
    ulat = row * gt[5] + gt[3]
    # Transform the point into the GeoTransform space
    (lon, lat, holder) = ct.TransformPoint(ulon, ulat)
    return (lat, lon)


def pixel_to_lat_lon_web_mercator(raster_dataset, col, row):
    spatial_reference = osr.SpatialReference()    
    spatial_reference.ImportFromWkt(raster_dataset.GetProjection())
    ds_spatial_reference_proj_string = spatial_reference.ExportToProj4()
    inProj = Proj(ds_spatial_reference_proj_string)
    outProj = Proj(init='epsg:3857')
    
    geo_transform = raster_dataset.GetGeoTransform()
    ulon = col * geo_transform[1] + geo_transform[0]
    ulat = row * geo_transform[5] + geo_transform[3]

    x2,y2 = transform(inProj,outProj,ulon,ulat)
    x2, y2 = outProj(x2,y2,inverse=True)
    print "{} {}".format(x2,y2)
    return x2,y2
