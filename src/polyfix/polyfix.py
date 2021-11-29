import fiona
from shapely.geometry import shape, MultiPolygon
from shapely.geometry.polygon import Polygon
from pathlib import PurePosixPath
from math import sqrt


def fix(polygon_path:str,output_path:str='', output_name:str=''):
    """
        creates polyfix object and call it's fix method,
        takes input path for spiked polygons and optionally output path and name, 
            if output path is not provided, the same path as the input is used, if name
            is not provided, it will be the input_name_corrected with the same file extension

            params:
            -----
            polygon_path(str): a path to the file contains polygon geometry, compatible file formats
            include gpkg, shp, GeoJSON, see https://fiona.readthedocs.io/en/latest/manual.html#data-model

            output_path(str): a path to output file, if not provided the same path as input is used.
            output_name(str): the name of the output file, if not provided, input name+ _corrected is used.
            
    """
    polyfix = Polyfix()
    polyfix.fix(polygon_path, output_path, output_name)

class Polyfix():
    def __init__(self) -> None:
        self.output_path = ''
        self.full_features_description = []
        self.driver = ''
        self.crs = ''
        self.schema = ''

    def fix(self,polygon_path:str,output_path:str='', output_name:str=''):
        """
            takes input path for spiked polygons and optionally output path and name, 
            if output path is not provided, the same path as the input is used, if name
            is not provided, it will be the input_name_corrected with the same file extension

            params:
            -----
            polygon_path(str): a path to the file contains polygon geometry, compatible file formats
            include gpkg, shp, GeoJSON, see https://fiona.readthedocs.io/en/latest/manual.html#data-model

            output_path(str): a path to output file, if not provided the same path as input is used.
            output_name(str): the name of the output file, if not provided, input name+ _corrected is used.
            
        """
        with fiona.open(polygon_path) as f:
            self.driver = f.driver
            self.crs = f.crs
            self.schema = f.schema
            features = list(f)
            self.full_features_description=features
            self.handle_multipart_features(features)
            file_output_name = ''
            if output_path=='':
                output_path_parent = PurePosixPath(polygon_path).parent
                suffix = PurePosixPath(polygon_path).suffixes[0]
                if output_name == '':
                    stem = PurePosixPath(polygon_path).stem
                    file_output_name = stem+'_corrected'
                else:
                    file_output_name = output_name
                output_path = PurePosixPath(output_path_parent).joinpath(f'{file_output_name}{suffix}')
            self.output_to_file(self.full_features_description, output_path)


    def output_to_file(self, output, output_path):
        """
            outputs the refined geometry to a file.

            params:
            -----
            output (collection): objects holding spatial data to be output to a file
            output_path(str): a path holds the information about the output file (path, name and extension)
        """
        output_path = str(output_path)
        
        with fiona.open(output_path,'w', driver=self.driver, crs=self.crs, schema=self.schema) as l:
            l.writerecords(output)


    def handle_multipart_features(self,features):
        """
            handles the presence of multipart geometries within the data via deconstructing to single parts.

            params:
            -----
            features (list): list of objects representing features read from fiona lib.
        """
        for feat in features:
            geometry_objects_with_ids =  self.get_single_parts(feat) # this can have a length of 1
            self.apply_fixer(geometry_objects_with_ids)


    def get_single_parts(self,feature)->list:
            """
                returns a list of single part geometry from multipart input.

                params:
                -----
                multipart (obj): and object holding the multipart geometry. 
            """
            feature_id = feature['id']
            
            if feature['geometry']['type'] == 'Polygon':
                polygon_geometry = Polygon(shape(feature['geometry']))
                return [{'id':feature_id,'geom':polygon_geometry}]
            
            elif feature['geometry']['type'] == 'MultiPolygon':
                multipolygon = MultiPolygon(shape(feature['geometry']))
                polygons_geometries = list(multipolygon)
                geoms_and_ids = self.link_geometries_to_id(polygons_geometries,feature_id)
                return geoms_and_ids
        
            else:
                raise TypeError('the geometry of this file is neither polygon nor multipolygon')


    def link_geometries_to_id(geometries:list, feature_id):
        """
            link geometries deconstructed by shapely with and ids for further ease of retrieval

            params:
            -----
            geometries(list): list of single part geometries.
            feature_id(int): an integer property of the input geometry. 
        """
        ob_list = []
        for geom in geometries:
            ob = {'id':id, 'geom':geom}
            ob_list.append(ob)
        return ob_list


    def apply_fixer(self,geometry_objects:list):
        """
            loops through geometry_objects and pass them to simple_spikes_fix 
            params:
            -----
            geometry_objects (list): list of geometries each accompanied by an id.  
        """
        for g in geometry_objects:
            self.simple_spikes_fix(g,10)


    def simple_spikes_fix(self,geometry_object,tolerance_value:float):
        """
            iterates over polygon objects coordinates and compares distances between points
            if the distance is greater than tolerance_value, it will be considered as a spike.
            
            params:
            -----
            geometry (shape): shapely geometry (polygon)
            tolerance (float): tolerance value -given according to data crs-, if the distance between a pair of exterior points is larger than the tolerance value, it is considered a spike
        """
        id = geometry_object['id']
        ex = list(geometry_object['geom'].exterior.coords)
        spikes, dist =[], 0
        ex_length = len(ex)
        for i in range(ex_length-2):
            current = i
            next = i+1
            dist = sqrt(pow(ex[current][0]-ex[next][0],2)+pow(ex[current][1]-ex[next][1],2))
            if dist>tolerance_value:
                spikes.append(ex[next])
        
        self.remove_spikes(id, ex,spikes)


    def remove_spikes(self, id, geometry_exterior_coords:list, spikes:list):
        """
            remove spike points (passed as an input) from the original data

            params:
            -----
            id(int): unique identifier for each geometry -- input with the data.
            geometry_exterior_coords(list): list of coordinates compared with spikes coords.
            spikes(list): list of spike points.
        """
        for i in spikes:
            if i in geometry_exterior_coords:
                geometry_exterior_coords.remove(i)
        
        self.refine_geoms(id,[geometry_exterior_coords])


    def refine_geoms(self,id,new_coords:list):
        """
            construct new geometry

            params
            -----
            id(int): unique identifier for each geometry -- input with the data.
            new_coords(list): new coordinate without spikes for constructing new geometries.
        """
        for i in self.full_features_description:
            if i['id'] == id:
                i['geometry']['coordinates'] = new_coords