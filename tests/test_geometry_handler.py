import sys
from pathlib import Path
from collections import OrderedDict
from shapely.geometry import Polygon

package_path = Path(__file__).parent.parent.joinpath('src/polyfix')
file_path = Path.cwd().parent.joinpath('testdata/spiky-polygons.gpkg')
sys.path.insert(0,(str(package_path)))
from geometry_handler import geomHandler

geomH = geomHandler()

polygon = {'type': 'Feature', 'id': '1', 'properties': OrderedDict([('name', 'test1')]), 'geometry': {'type': 'Polygon', 'coordinates': [[(18.5, -33.9), (18.6, -33.8), (18.7, -33.8)]]}}
multipolygon = {"type": "Feature", "geometry":{"type": "MultiPolygon","coordinates": [[[[30.0, 20.0], [45.0, 40.0], [10.0, 40.0], [30.0, 20.0]]], [[[15.0, 5.0], [40.0, 10.0], [10.0, 20.0], [5.0, 10.0], [15.0, 5.0]]]]}}


def test_get_single_parts_polygon():
    polygons_from_single_polygon = geomH.get_single_parts(polygon,1)
    assert polygons_from_single_polygon[0]['id'] == 1
    assert isinstance(polygons_from_single_polygon[0],object)
    assert isinstance(polygons_from_single_polygon[0]['geom'],Polygon)
    
def test_get_single_parts_multipolygon():
    polygons_from_multi_polygon = geomH.get_single_parts(multipolygon,1)
    first_polygon = polygons_from_multi_polygon[0]
    sec_polygon = polygons_from_multi_polygon[1]
    assert first_polygon['id'] == 1
    assert sec_polygon['id'] == 1
    assert isinstance(first_polygon['geom'],Polygon)
    assert isinstance(sec_polygon['geom'],Polygon)

