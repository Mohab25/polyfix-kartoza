import sys
from pathlib import Path
import json

package_path = Path(__file__).parent.parent.joinpath('src/polyfix')
sys.path.insert(0,(str(package_path)))
json_path = Path(__file__).parent.joinpath('geometries.json')
testdata = []
with open(json_path) as f:
    testdata = json.load(f)

points = testdata[0]['geometry']['coordinates'][0]

from angleFix import TriPairs
tri = TriPairs(points)

def test_create_nodes():
    tri.create_nodes()
    assert len(tri.nodesArray) > 0
    assert tri.nodesArray[0].index == 0
    assert tri.nodesArray[0].nextNodeIndex == 1
    assert tri.nodesArray[0].prevNodeIndex == len(tri.nodesArray)-1

def test_get_spikes():
    tri.create_nodes()
    spikes = tri.get_spikes(0.5)
    assert len(spikes) > 0
