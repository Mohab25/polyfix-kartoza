import sys
from pathlib import Path

package_path = Path(__file__).parent.parent.joinpath('src/polyfix')
sys.path.append(str(package_path))

from polyfixer import Polyfix
from polyfix_io import polyfixIO

polyfix_ob = Polyfix()

input_file = Path(__file__).parent.joinpath('testfolder/spiky-polygons.gpkg')  
input_file_multi_geom = Path(__file__).parent.joinpath('testfolder/multigeom.gpkg')  
corrected_file_path = Path(__file__).parent.joinpath('testfolder/fixed_function_out.gpkg')  
corrected_file_multi_geom = Path(__file__).parent.joinpath('testfolder/fixed_function_out_multigeom.gpkg')  

poly_io_features = polyfixIO(input_file)
poly_io_corrected_features = polyfixIO(corrected_file_path)

poly_io_features_multigeom = polyfixIO(input_file_multi_geom)
poly_io_corrected_features_multigeom = polyfixIO(corrected_file_multi_geom)


features = poly_io_features.get_features()
features_multigeom = poly_io_features_multigeom.get_features()

def test_fix():
    polyfix_ob.fix(input_file, 0.5, 2, '', 'fixed_function_out')
    output_file = Path(__file__).parent.joinpath('testfolder/fixed_function_out.gpkg')
    assert output_file.is_file()
    corrected_featrues = poly_io_corrected_features.get_features()
    assert features != corrected_featrues

def test_fix_multigeom():
    polyfix_ob.fix(input_file, 0.5, 2, '', 'fixed_function_out_multigeom')
    output_file = Path(__file__).parent.joinpath('testfolder/fixed_function_out_multigeom.gpkg')
    assert output_file.is_file()
    corrected_featrues = poly_io_corrected_features_multigeom.get_features()
    assert features_multigeom != corrected_featrues
