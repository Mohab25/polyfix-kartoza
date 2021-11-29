# polyfix-kartoza

fixing 'spikes' with polygon geometries

# Implementation

## class polyfix

## Methods

### apply_fixer

~~~py
def apply_fixer (self, geometry_objects: list)
~~~

loops through geometry_objects and pass them to simple_spikes_fix

~~~bash
params
------
geometry_objects (list): list of geometries each accompanied by an id.
~~~

### fix

~~~py
def fix(self, polygon_path: str, output_path: str = '', output_name: str = '')
~~~

takes input path for spiked polygons and optionally output path and name, if output path is not provided, the same path as the input is used, if name is not provided, it will be the input_name_corrected with the same file extension

~~~bash
params:
------
polygon_path(str): a path to the file contains polygon geometry, compatible file formats include gpkg, shp, GeoJSON, see https://fiona.readthedocs.io/en/latest/manual.html#data-model

output_path(str): a path to output file, if not provided the same path as input is used.

output_name(str): the name of the output file, if not provided, input name+ _corrected is used.
~~~

### get_single_parts

~~~py
def get_single_parts(self, feature) ‑> list
~~~

returns a list of single part geometry from multipart input.

~~~bash
params:
------
multipart (obj): and object holding the multipart geometry.
~~~

### handle_multipart_features

~~~py
def handle_multipart_features(self, features)
~~~

handles the presence of multipart geometries within the data via deconstructing to single parts.

~~~bash
params:
------
features (list): list of objects representing features read from fiona lib.
~~~

### link_geometries_to_id

~~~py
def link_geometries_to_id(geometries: list, feature_id)
~~~

link geometries deconstructed by shapely with and ids for further ease of retrieval

~~~bash
params:
------
geometries(list): list of single part geometries. feature_id(int): an integer property of the input geometry.
~~~

### output_to_file

~~~py
def output_to_file(self, output, output_path)
~~~

outputs the refined geometry to a file.

~~~bash
params:
------
output (collection): objects holding spatial data to be output to a file output_path(str): a path holds the information about the output file (path, name and extension)
~~~

### refine_geoms

~~~py
def refine_geoms(self, id, new_coords: list)
~~~

constructs new geometry

~~~bash
Params
------
id(int): unique identifier for each geometry – input with the data. new_coords(list): new coordinate without spikes for constructing new geometries.
~~~

### remove_spikes

~~~py
def remove_spikes(self, id, geometry_exterior_coords: list, spikes: list)
~~~

remove spike points (passed as an input) from the original data

~~~bash
params:
------
id(int): unique identifier for each geometry – input with the data. geometry_exterior_coords(list): list of coordinates compared with spikes coords. spikes(list): list of spike points.
~~~

### simple_spikes_fix

~~~py
def simple_spikes_fix(self, geometry_object, tolerance_value: float)
~~~

iterates over polygon objects coordinates and compares distances between points if the distance is greater than tolerance_value, it will be considered as a spike.

~~~bash
params:
------
geometry (shape): shapely geometry (polygon) tolerance (float): tolerance value -given according to data crs-, if the distance between a pair of exterior points is larger than the tolerance value, it is considered a spike
~~~
