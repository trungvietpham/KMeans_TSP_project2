import numpy as np

#Đổi tên thành Node
class Node:
    """
        Lớp chứa thông tin về 1 điểm, gồm: tọa độ, id, mảng chứa demand
    """
    def __init__(self, x, y, id, code, name, type, demand_array, cluster_id = None):
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
        self.code = code
        self.name = name
        self.type = type
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
    def __init__(self, id, capacity_list, v_type, coef):
        self.id = id
        self.capacity_list = capacity_list
        self.type = v_type
        self.coef = coef
    
    def __repr__(self):
        return "(" + str(self.id) + ")"



class Cluster:
    """
        Lớp chứa thông tin về 1 cụm, gồm: mảng sức chứa, mảng class City, số lượng items, mảng chứa trọng số hiện tại của cụm
    """
    def __init__(self, x, y, capacity_list, n_cities = 0, city_id_list = [], current_mass = None, scale_coef = 0, n_items = 2):
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
        if self.capacity_list is None: self.n_items = n_items
        elif len(self.capacity_list.shape) == 1: self.n_items = self.capacity_list.shape[0]
        else: self.n_items = self.capacity_list.shape[1]
        self.scale_coef = scale_coef
        if current_mass is None:
            self.current_mass = np.array(np.zeros((self.n_items))) # np.array chứa khối lượng hiện tại của cluster đối với từng loại mặt hàng
        else: self.current_mass = np.array(current_mass)
        # self.city_list = []
        # if (city_list != None):
        #     self.city_list = city_list
        #     for city in city_list:
        #         self.current_mass += city.demand_array
        self.n_cities = n_cities
        self.city_id_list = city_id_list
    
    def __del__(self):
        self.__del__
        # print('Destruction called')
        
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

    def print(self, location_flag = False, capa_flag = False, current_mass_flag = False, get_n_cities_flag = False, city_id_list_flag = False, header = ''):
        if location_flag: print('{}Location: {}'.format(header, self.get_center()))
        if capa_flag: print('{}Capacity list: {}'.format(header,self.capacity_list))
        if current_mass_flag: print('{}Current mass:  {}'.format(header,self.current_mass))
        if get_n_cities_flag: print('{}Num of city: {}'.format(header,self.n_cities))
        if city_id_list_flag: print('{}City id list: {}'.format(header, self.city_id_list))
