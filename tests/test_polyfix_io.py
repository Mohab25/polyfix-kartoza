import sys
from pathlib import Path
from collections import OrderedDict
package_path = Path(__file__).parent.parent.joinpath('src/polyfix')
file_path = Path(__file__).parent.parent.joinpath('testdata/spiky-polygons.gpkg')
sys.path.insert(0,(str(package_path)))
from polyfix_io import polyfixIO

polyfix_io_ob = polyfixIO(str(file_path))

def test_get_features():
    features = polyfix_io_ob.get_features()
    assert isinstance(features,list) == True
    
def test_unique_features():
    uni_features = polyfix_io_ob.get_unique_input_features()
    s= set()
    for i in uni_features:
        s.add(i['id']) # doesn't add duplicates
    
    assert len(uni_features) == len(s)


def test_output_to_file():
    output_folder = Path(__file__).parent.joinpath('testfolder/')
    Path.mkdir(output_folder, exist_ok=True)
    geojson_point = [{'type': 'Feature', 'id': '1', 'properties': OrderedDict([('name', 'test1')]), 'geometry': {'type': 'Polygon', 'coordinates': [[(18.5, -33.9), (18.6, -33.8), (18.7, -33.8)]]}}]
    polyfix_io_ob.output_to_file(geojson_point, output_folder,"test_correction" )
    test_file_path = output_folder.joinpath('test_correction.gpkg')
    assert test_file_path.is_file()
