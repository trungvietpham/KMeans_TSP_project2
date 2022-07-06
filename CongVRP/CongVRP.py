import numpy as np
from CongVRP.model import City
from CongVRP.utils import (clustering,
                            create_distance,
                            find_optimal_path,
                            edit)


class CongVRP:
    def __init__(self):
        self.distance_callback = None
        self.PickupAndDeliveryConstraint = {}

    def RegisterTransitCallback(self, distance_callback):
        """
        Register new function to define distance
        
        Args:

        `distance_callback` : The function to define distance
        
        Returns:
        """
        self.distance_callback = distance_callback
    
    def AddPickupAndDelivery(self, pickup_index : int, delivery_index : int):
        """
        Add a Pickup and Delivery requirement
        
        Args:

        `pickup_index` : Index of pickup city

        `dropCity`: Index of drop city
        
        Returns:

        """
        self.PickupAndDeliveryConstraint[pickup_index] = delivery_index

    def PickupAndDelivery(self, path):
        """
        Edit the path to satisfy Pickup and Delivery constraint


        Args:

        `path` : The path
        
        Returns:

        Path after editting
        """
        for constraint in self.PickupAndDeliveryConstraint.items():
            pickupCity = constraint[0]
            dropCity = constraint[1]
            path = edit(path, pickupCity, dropCity, self.distance_callback)
        return path

    def Congalgorithm(self, cluster, start, end, n_clusters = 15):
        """
        Find route for VRP
        
        Args:

        `cluster` : A cluster containing cities

        `start`: Index of start city

        `end` : Index of end city

        `n_clusters`: Number of cluster to cluster in each cluster
        
        Returns:

        The list of cities presenting the path 
        """
        if (cluster.get_quantity() == 1):
            return [cluster.city_list[0]]

        cluster_list = clustering(cluster, min(n_clusters, cluster.get_quantity()))
        distance = create_distance(cluster_list, self.distance_callback)
        start_cluster = None
        end_cluster = None
        for id, cluster_ in enumerate(cluster_list):
            for city in cluster_.city_list:
                if city.id == start:
                    start_cluster = id
                if city.id == end:
                    end_cluster = id
        path, cost = find_optimal_path(distance, start_cluster, end_cluster)
        final_path = []
        for id in range(len(path)):
            if (id == 0):
                start_ = start
                _, end_ = cluster_list[path[id]].distance(cluster_list[path[id + 1]], self.distance_callback)
            elif (id == len(path) - 1):
                _, start_ = cluster_list[path[id]].distance(cluster_list[path[id - 1]], self.distance_callback)
                end_ = end
            else:
                _, start_ = cluster_list[path[id]].distance(cluster_list[path[id - 1]], self.distance_callback)
                _, end_ = cluster_list[path[id]].distance(cluster_list[path[id + 1]], self.distance_callback)

            final_path = final_path + self.Congalgorithm(cluster_list[path[id]], start_, end_)

        return final_path
    
    def MultipleVehicles(self, path, num_vehicles):
        start = path[0]
        end = path[-1]
        num_each_vehicle = int(len(path) / num_vehicles)
        new_path = []
        for x in range(0, len(path), num_each_vehicle):
            new_path.append(path[x:x+num_each_vehicle]) 
        for id in range(len(new_path)):
            if id != 0:
                new_path[id].insert(0, start)
            if id != len(new_path) - 1:
                new_path[id].append(end)
        return new_path

    def find_route(self, cluster, start, end, n_clusters = 15):
        """
        Create route for VRP
        
        Args:

        `cluster` : A cluster containing cities

        `start`: Index of start city

        `end` : Index of end city

        `n_clusters`: Number of cluster to cluster in each cluster
        
        Returns:

        The list of cities presenting the path with pickup and delivery
        """

        final_path = self.Congalgorithm(cluster, start, end, n_clusters)
        final_path = self.PickupAndDelivery(final_path)
        return final_path