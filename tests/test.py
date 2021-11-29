import sys
from pathlib import Path
package_path = str(Path(__file__).parent.parent.joinpath('src/polyfix'))
print(package_path)
sys.path.insert(0,package_path)
from polyfix import fix

def test_output_files():
    file_path = Path().resolve().parent.joinpath('testdata/spiky-polygons.gpkg')
    output_file_path = Path(__file__).parent.parent.joinpath('testdata/spiky-polygons_corrected.gpkg')
    assert output_file_path.is_file() == False
    fix(file_path)
    assert output_file_path.is_file() == True
