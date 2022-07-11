import numpy as np

#Đổi tên thành Node
class Node:
    """
        Lớp chứa thông tin về 1 điểm, gồm: tọa độ, id, mảng chứa demand
    """
    def __init__(self, x, y, id, demand_array, cluster_id = None):
        """
        Get the number of city in this cluster
        
        Args:

        `x`: The value of latitude

        `y`: The value of longtitude
        
        `id`: Index of the city (number or string)

        `demand_array`: np.array chứa demand về từng mặt hàng

        Returns:

        """
        self.x = x
        self.y = y
        self.id = id
        self.demand_array = demand_array
        self.cluster_id = None
        if cluster_id is not None: self.cluster_id = cluster_id
    
    def __repr__(self):
        return "(" + str(self.id) + ")"

    def get_location(self):
        return [self.x, self.y]

    def print(self, id_flag = False, location_flag = False, demand_flag = False, cluster_id_flag = False):
        if id_flag: print('Id: {}'.format(self.id))
        if location_flag: print('Location: ({}, {})'.format(self.x, self.y))
        if demand_flag: print('Demand: {}'.format(self.demand_array))
        if cluster_id_flag: print('Cluster ID: {}'.format(self.cluster_id))


class Vehicle:
    '''
    Lớp chứa thông tin về 1 xe, gồm: id, mảng sức chứa tối đa đối với mỗi mặt hàng
    '''
    def __init__(self, id, capacity_list):
        self.id = id
        self.capacity_list = capacity_list
    
    def __repr__(self):
        return "(" + str(self.id) + ")"



class Cluster:
    """
        Lớp chứa thông tin về 1 cụm, gồm: mảng sức chứa, mảng class City, số lượng items, mảng chứa trọng số hiện tại của cụm
    """
    def __init__(self, x, y, capacity_list, n_items = 2, n_cities = 0, city_id_list = []):
        """
        Get the number of city in this cluster
        
        Args:
        `x, y`: Tọa độ của tâm cụm
        `capacity_list`: np.array gồm khối lượng tối đa mà cluster này được gán cho đối với mỗi mặt hàng (trong 2 mặt hàng)
        `city_list`: list class City các thành phố trong cluster này

        Returns:

        """
        self.x = x
        self.y = y
        self.capacity_list = capacity_list
        self.n_items = n_items
        self.current_mass = np.array(np.zeros((n_items))) # np.array chứa khối lượng hiện tại của cluster đối với từng loại mặt hàng
        # self.city_list = []
        # if (city_list != None):
        #     self.city_list = city_list
        #     for city in city_list:
        #         self.current_mass += city.demand_array
        self.n_cities = n_cities
        self.city_id_list = city_id_list
        
    def get_center(self):
        return [self.x, self.y]

    def set_center(self, center):
        self.x = center[0]
        self.y = center[1]

    # def clear_city(self):
    #     self.city_list = []
    #     self.current_mass = np.array(np.zeros((self.n_items)))
    def append_city(self, city_id):
        self.city_id_list.append(city_id)

    def update_mass(self, add_mass, city_id):
        self.current_mass+=add_mass
        self.n_cities+=1
        self.append_city(city_id)
    
    def clear_mass(self):
        self.current_mass = np.array(np.zeros(self.n_items))
        self.n_cities = 0
        self.city_id_list = []
        
    # def get_quantity(self):
    #     """
    #     Get the number of city in this cluster
        
    #     Args:
        
    #     Returns:

    #     The number of city
    #     """
    #     return len(self.city_list)


    # def append(self, city: City):
    #     """
    #     Append a new city into this cluster
        
    #     Args:
        
    #     Returns:
    #     """
    #     #print(type(self.city_list))
    #     print('City list: {}'.format(a.id for a in self.city_list))
    #     self.city_list.append(city)
    #     self.current_mass = self.current_mass + city.demand_array


    # def distance(self, cluster, distance_callback):
    #     """
    #     Calculate the distance between 2 clusters

    #     Args:

    #     `cluster`: Cluster you want to cal distance

    #     `distance_callback`: The function defining the distance between 2 city
        
    #     Returns:

    #     The distance between 2 cluster
    #     Được tính bằng khoảng cách nhỏ nhất giữa 2 thành phố thuộc 2 cụm
    #     Trả về: khoảng cách đã tính được, id thành phố của cluster kia

    #     """
    #     min_distance = np.inf
    #     city_list = cluster.city_list
    #     connect_city = None
        
    #     for beg in self.city_list:
    #         for des in city_list:
    #             distance = distance_callback(beg, des)
    #             if min_distance > distance:
    #                 min_distance = distance
    #                 connect_city = beg.id
        
    #     return min_distance, connect_city

    def print(self, location_flag = False, capa_flag = False, current_mass_flag = False, get_n_cities_flag = False, city_id_list_flag = False, header = ''):
        if location_flag: print('{}Location: {}'.format(header, self.get_center()))
        if capa_flag: print('{}Capacity list: {}'.format(header,self.capacity_list))
        if current_mass_flag: print('{}Current mass:  {}'.format(header,self.current_mass))
        if get_n_cities_flag: print('{}Num of city: {}'.format(header,self.n_cities))
        if city_id_list_flag: print('{}City id list: {}'.format(header, self.city_id_list))
