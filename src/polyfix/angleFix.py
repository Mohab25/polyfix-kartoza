from math import sqrt, acos

class Node():
    def __init__(self, point) -> None:
        self.point = point
        self.index = None
        self.prevNodeIndex = None
        self.nextNodeIndex = None

class TriParis():
    def __init__(self, data) -> None:
        self.data = data
        self.nodesArray = []
    
    def create_nodes(self):
        """
            creates a linked list of Node objects.

            params:
            -----
            None
        """
        for index, point in enumerate(self.data[0:-1],start=0):
            node = Node(point)
            node.index = index
            prevIndex = index-1
            nextIndex = index+1
            if prevIndex <0:
                node.prevNodeIndex = len(self.data)-2
            else:
                node.prevNodeIndex = prevIndex
            if nextIndex > len(self.data)-2:
                node.nextNodeIndex = 0
            else:
                node.nextNodeIndex = nextIndex
            
            self.nodesArray.append(node)


    def get_spikes(self,threshold: float) -> list:
        """
            creates angle between each node and it's 
            next and previous nodes, if the angle is
            less than a given threshold, the node
            is considered a spike.

            params:
            -----
            threshold(float): the minimum angle
            afterwhich the value is considered
            a spike 
        """
        angles = []
        spikes = []
        for i in self.nodesArray:
            prev = self.nodesArray[i.prevNodeIndex]
            next = self.nodesArray[i.nextNodeIndex]
            l1 = sqrt(pow(next.point[0]-prev.point[0],2)+pow(next.point[1]-prev.point[1],2))
            l2 = sqrt(pow(i.point[0]-prev.point[0],2)+pow(i.point[1]-prev.point[1],2))
            l3 = sqrt(pow(i.point[0]-next.point[0],2)+pow(i.point[1]-next.point[1],2))
            angle = acos((pow(l2,2)+pow(l3,2)-pow(l1,2))/(2*l2*l3))
            angles.append(angle)
            if angle < threshold:
                spikes.append(i.point)
        return spikes


