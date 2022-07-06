import numpy as np

class City:
    """
        A class for a location
    """
    def __init__(self, x, y, id):
        """
        Get the number of city in this cluster
        
        Args:

        `x`: The value of X-axis

        `y`: The value of Y-axis

        `id`: Index of the city

        Returns:

        """
        self.x = x
        self.y = y
        self.id = id
    
    def __repr__(self):
        return "(" + str(self.id) + ")"

class Cluster:
    """
        A class for a cluster
    """
    def __init__(self, city_list = None):
        """
        Get the number of city in this cluster
        
        Args:

        `city_list`: The list containing cities in a cluster

        Returns:

        """
        self.city_list = []
        if (city_list != None):
            self.city_list = city_list
    
    def get_quantity(self):
        """
        Get the number of city in this cluster
        
        Args:
        
        Returns:

        The number of city
        """
        return len(self.city_list)

    def append(self, city):
        """
        Append a new city into this cluster
        
        Args:
        
        Returns:
        """
        self.city_list.append(city)

    def distance(self, cluster, distance_callback):
        """
        Calculate the distance between 2 clusters

        Args:

        `cluster`: Cluster you want to cal distance

        `distance_callback`: The function defining the distance between 2 city
        
        Returns:

        The distance between 2 cluster

        """
        min_distance = np.inf
        city_list = cluster.city_list
        connect_city = None
        
        for beg in self.city_list:
            for des in city_list:
                distance = distance_callback(beg, des)
                if min_distance > distance:
                    min_distance = distance
                    connect_city = beg.id
        
        return min_distance, connect_city

