from math import sqrt
from .angleFix import TriParis
from .polyfix_io import polyfixIO
from .geometry_handler import geomHandler

def fix(polygon_path: str, tolerance_value: float, output_path: str = '', output_name: str = ''):
    """
        an interface for polyfix.fix - see below
    """
    polyfix = Polyfix()
    polyfix.fix(polygon_path, tolerance_value, output_path, output_name)

class Polyfix():
    def __init__(self) -> None:
        self.input_features = []
        self.output_features=[]
        self.driver = ''
        self.crs = ''
        self.schema = ''

    def fix(self, polygon_path: str, tolerance_value: float, output_path: str = '',
            output_name: str = ''):
        """
            takes input path for spiked polygons and optionally
            output path and name, if output path is not provided,
            the same path as the input is used, if name is not provided,
            input_name_corrected is used with the same file extension.

            params:
            -----
            polygon_path(str): a path to the file contains polygon geometry,
            compatible file formats include gpkg, shp, GeoJSON,
            see https://fiona.readthedocs.io/en/latest/manual.html#data-model

            output_path(str): a path to output file, if not provided the same
            path as input is used.
            output_name(str): the name of the output file, if not provided,
            input name+ _corrected is used.
        """
        io_control = polyfixIO(polygon_path)
        features = io_control.get_features()
        self.input_features = io_control.get_input_features()
        self.handle_multipart_features(features, tolerance_value)
        io_control.output_to_file(self.output_features, output_path, output_name)

    def handle_multipart_features(self, features, tolerance_value):
        """
            handles the presence of multipart geometries
            within the data via deconstructing to
            single parts.

            params:
            -----
            features (list): list of objects representing
            features read from fiona lib.
        """
        geom_handler = geomHandler()
        for index, feat in enumerate(features, start = 0):
            geometry_objects_with_ids = geom_handler.get_single_parts(feat, index)
            self.apply_fixer(geometry_objects_with_ids, tolerance_value)

    def apply_fixer(self, geometry_objects: list, tolerance_value, algo: int = 2):
        """
            loops through geometry_objects and pass them
            to simple_spikes_fix method.

            params:
            -----
            geometry_objects (list): list of geometries,
            each accompanied by an id.
        """
        for g in geometry_objects:
            if algo == 2:
                self.angle_fix(g, tolerance_value)
            else:
                self.simple_spikes_fix(g, tolerance_value)

    def simple_spikes_fix(self, geometry_object, tolerance_value: float):
        """
            iterates over polygon objects coordinates
            and compares distances between points
            if the distance is greater than tolerance_value,
            it will be considered as a spike.

            params:
            -----
            geometry (shape): shapely geometry (polygon)
            tolerance (float): tolerance value -given according
            to data crs-, if the distance between a pair of
            exterior points is larger than the tolerance value,
            it is considered a spike
        """
        id = geometry_object['id']
        ex = list(geometry_object['geom'].exterior.coords)
        spikes, dist = [], 0
        ex_length = len(ex)
        for i in range(ex_length-2):
            current = i
            next = i+1
            dist = sqrt(pow(ex[current][0]-ex[next][0], 2)+pow(ex[current][1]-ex[next][1], 2))
            if dist > tolerance_value:
                spikes.append(ex[next])
        self.remove_spikes(id, ex, spikes)

    def angle_fix(self, geometry_object, tolerance_value: float):
        """"
            apply another algorithm based on the angle
            between current point and next/prev points
        """
        id = geometry_object['id']
        data = list(geometry_object['geom'].exterior.coords)
        tri = TriParis(data)
        tri.create_nodes()
        spikes = tri.get_spikes(tolerance_value)
        self.remove_spikes(id, data, spikes)

    def remove_spikes(self, id, geometry_exterior_coords: list, spikes: list):
        """
        remove spike points (passed as an input) from
        the original data

        params:
        -----
        id(int): unique identifier for each geometry
        -- input with the data.
        geometry_exterior_coords(list): list of coordinates
        compared with spikes coords.
        spikes(list): list of spike points.
        """
        for i in spikes:
            if i in geometry_exterior_coords:
                geometry_exterior_coords.remove(i)

        self.refine_geoms(id, [geometry_exterior_coords])

    def refine_geoms(self, id, new_coords: list):
        """
        construct new geometry

        params
        -----
        id(int): unique identifier for each
        geometry -- input with the data.
        new_coords(list): new coordinate
        without spikes for constructing
        new geometries.
        """
        for i in self.input_features:
            if i['id'] == id:
                i['feat']['geometry']['coordinates'] = new_coords
            
            self.output_features.append(i['feat'])
