from math import sqrt
from .angleFix import TriPairs


class Fixer():

    def __init__(self) -> None:
        pass

    def apply_fixer(self, geometry_objects: list, tolerance_value, algorithm_type: int = 2):
        """
            loops through geometry_objects and pass them
            to simple_spikes_fix method.

            params:
            -----
            geometry_objects (list): list of geometries,
            each accompanied by an id.
        """
        for g in geometry_objects:
            if algorithm_type == 2:
                return self.angle_fix(g, tolerance_value)
            else:
                return self.simple_spikes_fix(g, tolerance_value)

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
        return self.remove_spikes(id, ex, spikes)

    def angle_fix(self, geometry_object, tolerance_value: float):
        """"
            apply an algorithm based on the angle
            between current point and next/prev points,
            if the angle is greater than a threshold
            value the middle point is considered a spike.

            params:
            -----
            geometry (shape): shapely geometry (polygon)
            tolerance_value (float): tolerance value
            -given according to data crs-,
            if the distance between a pair of exterior
            points is larger than the tolerance value,
            it is considered a spike.
        """
        id = geometry_object['id']
        data = list(geometry_object['geom'].exterior.coords)
        tri = TriPairs(data)
        tri.create_nodes()
        spikes = tri.get_spikes(tolerance_value)
        return self.remove_spikes(id, data, spikes)

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
        spikes(list): list of spiked points.
        """
        for i in spikes:
            if i in geometry_exterior_coords:
                geometry_exterior_coords.remove(i)

        return {"id": id, "new_coords": [geometry_exterior_coords]}
