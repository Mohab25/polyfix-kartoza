from shapely.geometry import shape, Polygon, MultiPolygon

class geomHandler():

    def __init__(self) -> None:
        pass

    def get_single_parts(self, feature, index) -> list:
            """
                returns a list of single part geometry from
                multipart input.

                params:
                -----
                multipart (obj): and object holding the
                multipart geometry.
            """
            feature_id = index
            if feature['geometry']['type'] == 'Polygon': 
                polygon_geometry = Polygon(shape(feature['geometry']))
                return [{'id': feature_id, 'geom': polygon_geometry}]

            elif feature['geometry']['type'] == 'MultiPolygon':
                multipolygon = MultiPolygon(shape(feature['geometry']))
                polygons_geometries = list(multipolygon)
                geoms_and_ids = self.link_multi_geometries_to_one_id(polygons_geometries,feature_id)
                return geoms_and_ids

            else:
                raise TypeError("the geometry of this file is"
                                "neither polygon nor multipolygon")

    def link_multi_geometries_to_one_id(self, geometries: list, feature_id: int):
        """
            link geometries deconstructed by shapely with
            ids for further ease of retrieval

            params:
            -----
            geometries(list): list of single part
            geometries.

            feature_id(int): an integer property of the
            input geometry.
        """
        ob_list = []
        for geom in geometries:
            ob = {'id': feature_id, 'geom': geom}
            ob_list.append(ob)

        return ob_list
