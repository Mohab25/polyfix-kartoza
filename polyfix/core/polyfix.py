import fiona
from shapely.geometry import shape, MultiPolygon
from shapely.geometry.polygon import Polygon
from math import sqrt


class polyfix():
    def __init__(self,file_path:str) -> None:
        self.file_path = file_path
        self.full_features_description = []
        self.driver = ''
        self.crs = ''
        self.schema = ''

    def output_to_file(self,output):
        """
            outputs the refined geometry to a file with the same path and different name.
        """
        with fiona.open('/home/mohab/Kartoza/assignment/output.gpkg','w', driver=self.driver, crs=self.crs, schema=self.schema) as l:
            l.writerecords(output)

    def refine_geoms(self,id,new_coords:list):
        """
            construct new geometries
        """
        #print('\n this is the list: \n', self.full_features_description)
        #print('=============================================================')
        for i in self.full_features_description:
            if i['id'] == id:
                #print('this is the item: \n',i)
                i['geometry']['coordinates'] = new_coords
                #print('\n this is the updated item \n',i)
            
        # print('=============================================================')
        
        print('\n this is the updated list: \n', self.full_features_description)

        # print('*******************************************************************')
    
        

    def remove_spikes(self, id, geometry_exterior_coords:list, spikes:list):
        """
            remove spike points from the geometry definition
        """
        for i in spikes:
            if i in geometry_exterior_coords:
                geometry_exterior_coords.remove(i)
        
        self.refine_geoms(id,[geometry_exterior_coords])

    def simple_spikes_fix(self,geometry_object,tolerance_value:float):
        """
            iterate over the polygon coords, compare distances between points

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

    def apply_fixer(self,geometry_objects:list):
        """
            check the validity of geometries and call fixers if the geometry is not valid

            params:
            -----
            geometries (list): list of geometries (using shapely constructs)  
        """
        for g in geometry_objects:
            self.simple_spikes_fix(g,10)
        

    def handle_multipart_features(self,features):
        """
            takes a list of features and loop through each while applying other functions

            params:
            -----
            features (list): list of objects representing features read by fiona
        """
        for feat in features:
            geometry_objects_with_ids =  self.get_single_parts(feat) # this can have a length of 1
            self.apply_fixer(geometry_objects_with_ids)



    def link_geometries_to_id(geometries:list, feature_id):
        """
            link geometries deconstructed by shapely with and id for further retrieval
        """
        ob_list = []
        for geom in geometries:
            ob = {'id':id, 'geom':geom}
            ob_list.append(ob)
        return ob_list

    def get_single_parts(self,feature)->list:
        """
            takes a multipart geometry feature -read by fiona- and returns a list of it's parts

            params:
            -----
            multipart (obj): and object holding the multipart geometry 
        """
        feature_id = feature['id']
        
        if feature['geometry']['type'] == 'Polygon':
            polygon_geometry = Polygon(shape(feature['geometry']))
            return [{'id':feature_id,'geom':polygon_geometry}]
        
        elif feature['geometry']['type'] == 'MultiPolygon':
            multipolygon = MultiPolygon(shape(feature['geometry']))
            polygons_geometries = list(multipolygon)
            geoms_and_ids = self.link_geometries_to_id(polygons_geometries,feature_id)
            # this needs to change so each geometry must be accompanied with an id.
            return geoms_and_ids
        
        else:
            raise TypeError('the geometry of this file is neither polygon nor multipolygon')


    def fix(self):
        with fiona.open(self.file_path) as f:
            self.driver = f.driver
            self.crs = f.crs
            self.schema = f.schema
            features = list(f)
            self.full_features_description=features
            self.handle_multipart_features(features)
            self.output_to_file(self.full_features_description)

f = polyfix('/home/mohab/Kartoza/assignment/testdata/spiky-polygons.gpkg')
f.fix()