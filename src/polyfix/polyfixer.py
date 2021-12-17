from polyfix_io import polyfixIO
from geometry_handler import geomHandler
from fixers import Fixer


def fix(polygon_path: str, tolerance_value: float,
        output_path: str = '', output_name: str = ''):
    """
        an interface for polyfix.fix - see below
    """
    polyfix = Polyfix()
    polyfix.fix(polygon_path, tolerance_value, output_path, output_name)


class Polyfix():
    def __init__(self) -> None:
        self.input_features = []
        self.output_features = []
        self.driver = ''
        self.crs = ''
        self.schema = ''

    def fix(self, polygon_path: str, tolerance_value: float,
            algorithm_code: int = 2, output_path: str = '',
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
        """
        io_control = polyfixIO(polygon_path)
        features = io_control.get_features()
        self.input_features = io_control.get_unique_input_features()
        self.handle_multipart_features(features, tolerance_value, algorithm_code)
        io_control.output_to_file(self.output_features, output_path, output_name)

    def handle_multipart_features(self, features: list, tolerance_value: float, algorithm_code: int):
        """
            deconstruct multipart geometries into single
            parts for futher processing.
            params:
            -----
            features (list): list of geo-features
            as they are read from .gpkg file
            tolerance_value(float): the value
            which will be used as a threshold
            for removing spikes.
            algorithm_code: an integer that defines
            which algorithm will be used for removing
            spikes
        """
        geom_handler = geomHandler()
        for index, feat in enumerate(features, start=0):
            geometry_objects_with_ids = geom_handler.get_single_parts(feat, index)
            fixer = Fixer()
            new_geom_ob = fixer.apply_fixer(geometry_objects_with_ids, tolerance_value, algorithm_code)
            self.refine_output_geom(new_geom_ob)

    def refine_output_geom(self, new_geom: object):
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
            if i['id'] == new_geom['id']:
                i['feat']['geometry']['coordinates'] = new_geom['new_coords']

            self.output_features.append(i['feat'])
