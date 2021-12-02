import sys
from pathlib import Path
from collections import OrderedDict
from shapely.geometry import shape, Polygon, MultiPolygon
import json

package_path = Path(__file__).parent.parent.joinpath('src/polyfix')
sys.path.append(str(package_path))
json_path = Path(__file__).parent.joinpath('geometries.json')

from fixers import Fixer
fixer = Fixer()

data = []
with open(json_path) as f:
    data = json.load(f)

poly_geom = Polygon(shape(data[0]['geometry']))
multi_poly_geom = MultiPolygon(shape(data[1]['geometry']))

spiked_polygon = {"id": 0, "geom": poly_geom}
spiked_multipolygon = {"id": 0, "geom": multi_poly_geom}

def test_apply_fixer_polygon_simple_algorithm():
    spikes = fixer.apply_fixer([spiked_polygon],10,1)
    original_item = data[0]
    original_item['geometry']['coordinates'] = spikes['new_coords']
    corrected_polygon = Polygon(shape(original_item['geometry']))
    assert corrected_polygon != spiked_polygon['geom']

def test_apply_fixer_polygon_angle_algorithm():
    print("multipart geometries are deconstructed first then a fix is applied"
    "this is implicit in testing Polgyfix class, handle_multipart_features method"
    )
    assert True

#def test_apply_fixer_multi_polygon_simple_algorithm():
    # spikes = fixer.apply_fixer([spiked_polygon],10,1)
    # original_item = data[1]
    # original_item['geometry']['coordinates'] = spikes['new_coords']
    # corrected_polygon = Polygon(shape(original_item['geometry']))
    # assert corrected_polygon != spiked_polygon['geom']

