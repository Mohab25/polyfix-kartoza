# polyfix-kartoza

fixing 'spikes' with polygon geometries

# Installation

use the following command to install the lib

~~~bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple kartoza-polyfix==0.1.4.3
~~~

# Usage

the library API defines only one method "fix", used to fix the spiked geometry

~~~py
from polyfix import fix
fix('file_path')
~~~

for the implementation of fix and other options, see [fix](#fix) 
# Implementation

## class polyfix_io

mainly responsible for inputs (file reading), and output operations.

~~~bash
attributes:
---------
file_path (str): path ot the file.
driver (str): OGR driver name used for proper file read and creation. 
crs (obj): coordinate reference system for data input / output.
schema (obj): schema of input data (it's attributes and geometry), used to input/output data. 
~~~

## Methods

### get_features

~~~py
def get_features(self)-> list
~~~

read the geo-file and geographic features.

~~~bash
params:
-----
None
~~~

### get__unique_input_features

~~~py
def get__unique_input_features(self) -> list
~~~

gives each input feature a unique id.

~~~bash
params:
-----
None
~~~

### output_to_file

~~~py
output_to_file(self, output, output_path :Path = '', output_name :str = '' )
~~~

output newly created and corrected geographic features to a file

~~~bash
params:
-----
output (collection): objects holding spatial data
which to be output to a file
output_path(Path): a path holds the information about
the output file (path, name and extension)
~~~

## class polyfix

this is the base class responsible for controlling operations over data.

~~~bash
attributes:
---------
input_features(list) : list of input geographic features.
output_features(list): list of refined geometries to output to a file.
driver (str): OGR driver name used for proper file read and creation. 
crs (obj): coordinate reference system for data input / output.
schema (obj): schema of input data (it's attributes and geometry), used to input/output data. 
~~~

## Methods

### fix

~~~py
def fix(self, polygon_path: str, tolerance_value: float, algorithm_code: int = 2, output_path: str = '',
            output_name: str = '')
~~~

takes input path for spiked polygons and optionally
output path and name, if output path is not provided,
the same path as the input is used, if name is not provided,
input_name_corrected is used with the same file extension.

~~~bash
params:
-----
polygon_path(str): a path to the file contains polygon geometry,
compatible file formats include gpkg, shp, GeoJSON,
see https://fiona.readthedocs.io/en/latest/manual.html#data-model
tolerance_value(float): value of the threshold upon which
spikes are defined, according to algorithm type, the tolerance
can either be an angle threshold (in degrees), or a distance 
threshold (map unit).
algorithm_code: the algorithm to be used to identify and remove
spikes, currently two algorithms are used, based on distance
(code 1), or based on angles (code 2 - default).
output_path(str): a path to output file, if not provided the same
path as input is used.
output_name(str): the name of the output file, if not provided,
input name+ _corrected is used.
~~~

### handle_multipart_features

~~~py
def handle_multipart_features(self, features: list, tolerance_value: float, algorithm_code: int)
~~~

deconstruct multipart geometries into single parts for further processing.

~~~bash

params:
-----
features (list): list of geo-features
as they are read from geo files
tolerance_value(float): the value
which will be used as a threshold
for removing spikes.
algorithm_code: an integer that defines
which algorithm will be used for removing
spikes
~~~

### refine_output_geom

~~~py
def refine_output_geom(self, new_geom: object):
~~~

alter existing geometry -which holds spikes- with new refined geometry, that will be output to  a new file.

~~~bash
Params
------
new_geom (object): and object holds both the new coordinates and an id to identify the refined geometry.
~~~

## class geomHandler

used to deconstruct multipart geometries into single parts.

~~~bash
attributes:
---------
None
~~~

## Methods

### get_single_parts

~~~py
def get_single_parts(self, feature, index) -> list
~~~

returns a list of single part geometries from multipart input.

~~~bash
params:
------
feature (obj): an object holding the
multipart geometry.
index (int): a unique number attached to the geometries.
~~~

### link_multi_geometries_to_one_id

~~~py
def link_multi_geometries_to_one_id(self, geometries: list, feature_id: int)
~~~

link multipart geometries deconstructed by shapely with an id for further ease of retrieval.

~~~bash
params:
------
geometries(list): list of single part geometries. 
feature_id(int): an integer property of the input geometry.
~~~

## class Fixer

responsible for applying spikes removal algorithms on geographic features.

~~~bash
attributes:
---------
None
~~~

## Methods

### apply_fixer

~~~py
def apply_fixer(self, geometry_objects: list, tolerance_value, algorithm_type: int = 2):
~~~

loops through geometry objects and pass them to fixing algorithm.

~~~bash
params
------
geometry_objects (list): list of geometries each accompanied by an id.
tolerance_value(float): value of the threshold upon which
spikes are defined, according to algorithm type, the tolerance
can either be an angle threshold (in degrees), or a distance 
threshold (map unit).
algorithm_code(int): the algorithm to be used to identify and remove
spikes, currently two algorithms are used, based on distance
(code 1), or based on angles (code 2 - default).
~~~

### simple_spikes_fix

~~~py
def simple_spikes_fix(self, geometry_object, tolerance_value: float):
~~~

iterates over polygon objects coordinates
and compares distances between points to the tolerance_value
if the distance is greater than tolerance_value,
it will be considered as a spike.

~~~bash
params:
------
geometry (shape): shapely geometry (polygon) 
tolerance_value (float): tolerance value -given according to data crs-,
if the distance between a pair of exterior points is larger than the tolerance value,
it is considered a spike.
~~~

### angle_fix

~~~py
def angle_fix(self, geometry_object, tolerance_value: float)
~~~

apply an algorithm based on the angle
between current point and next/prev points,
if the angle is greater than a threshold 
value the middle point is considered a spike.

~~~bash
params:
------
geometry (shape): shapely geometry (polygon) 
tolerance_value (float): tolerance value -given according to data crs-, 
if the distance between a pair of exterior points is larger than the tolerance value,
it is considered a spike.
~~~

### remove_spikes

~~~py
def remove_spikes(self, id, geometry_exterior_coords: list, spikes: list):
~~~

remove spike points (passed as an input) from the original data

~~~bash
params:
------
id(int): unique identifier for each geometry – input with the data. 
geometry_exterior_coords(list): list of coordinates compared with spikes coords. 
spikes(list): list of spiked points.
~~~

## class Node

hold the data structure for nodes used with angles-based correction algorithm.

~~~bash
attributes:
---------
point (list): coordinates of an input geometry point
index (int): a unique identifier for each geometry.
prevNodeIndex(int): a unique identifier for each geometry 
-- used to link each geometry with others (previous).
nextNodeIndex(int): a unique identifier for each geometry 
-- used to link each geometry with others (next).
~~~

## class TriParis

creates a network of pairs of coordinates where each holds three points,
applies an angle-based algorithm between points to identify spikes.

~~~bash
attributes:
---------
data (list): a list of input geometries.
nodesArray (list): a list of Nodes objects.
~~~

## Methods

### create_nodes

~~~py
def create_nodes(self)-> None:
~~~

creates a linked list of Node objects.

~~~bash
params:
-----
None
~~~

### get_spikes

~~~py
def get_spikes(self,threshold:float)->list
~~~

creates angle between each node and it's
next and previous nodes, if the angle is
less than a given threshold, the node
is considered a spike.

~~~bash
params:
-----
threshold(float): the minimum angle
after which the value is considered
a spike 
~~~
