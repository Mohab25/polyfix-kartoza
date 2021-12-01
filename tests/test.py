import sys
from pathlib import Path
package_path = Path.cwd().parent.joinpath('src')
print(package_path)

sys.path.insert(0,(str(package_path)))
from polyfix import fix

def test_output_files():
    file_path = Path.cwd().parent.joinpath('testdata/spiky-polygons.gpkg')
    output_file = Path.cwd().parent.joinpath('testdata/spiky-polygons_corrected.gpkg')
    assert output_file.is_file() == False
    fix(file_path)
    assert output_file.is_file() == True
