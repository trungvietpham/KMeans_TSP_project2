import numpy as np
from scipy.spatial import distance
import re
import sys

from sklearn.utils import shuffle
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from SupportClass import Vehicle, Node, Cluster

def manhattan_distance(p1, p2):
    '''
    Params: nhận vào tọa độ 2 điểm
    Return: Khoảng cách giữa 2 điểm tính theo l1-norm
    '''
    return np.sum(np.abs(np.array(p1) - np.array(p2)))

def optimizer(city_list, cluster_list, alpha, penalty_coef):
    '''
    Params:
    city_list: list class City
    cluster_list: list class Cluster
    Return:
    Trả về dạng 1 mảng n_city hàng, n_clusters cột
    Trả về 1 mảng labels n_city hàng

    Dạng hàm: L1(city_i, center_j) - alpha*(chuyên chở - trọng số)
    '''
    n_cities = len(city_list)
    n_clusters  = len(cluster_list)

    #Shuffle cities:
    shuffle_index = [i for i in range(n_cities)]
    shuffle_index = shuffle(shuffle_index)
    city_list_shuffle = [city_list[i] for i in shuffle_index]

    labels = []
    result_array = np.zeros((n_cities, n_clusters))
    for i in range(n_cities):
        for j in range(n_clusters):
            result_array[i,j] = manhattan_distance(city_list_shuffle[i].get_location(), cluster_list[j].get_center()) 

            remain_capa = np.array(cluster_list[j].capacity_list) - np.array(cluster_list[j].current_mass) - city_list_shuffle[i].demand_array
            tmp = 0.0
            for remain in remain_capa: 
                if remain>0: tmp+=remain
                else: tmp+=penalty_coef*remain

            tmp = tmp/np.sum(np.array(cluster_list[j].capacity_list))
            result_array[i,j] -= alpha*tmp
            print('Res[{}, {}] = {}'.format(i,j,result_array[i,j]))

        labels.append(np.argmin(result_array[i]))
        print('Assign to cluster {}'.format(labels[-1]))
        print('Before assign: ')
        for k in range(n_clusters):
            print('Cluster {}: '.format(k))
            cluster_list[k].print()
        (cluster_list[labels[-1]]).update_mass(city_list_shuffle[i].demand_array)
        city_list_shuffle[i].cluster_id = labels[-1]

        print('After assign: ')
        for k in range(n_clusters): 
            print('Cluster {}: '.format(k))
            cluster_list[k].print()
    
    return (result_array, np.array(labels))

def load_vehicle_from_text(file_name):
    '''
    Params: 
    file_name: đường dẫn tới file text
    định dạng file text: 
    line 1: số lượng xe n
    n line tiếp theo: sức chuyên chở của từng xe đối với từng loại mặt hàng
    Return:

    '''
    with open(file_name, 'r') as f:
        data = f.read()
    data = data.split('\n')
    n_vehicles = int(data[0])
    vehicle_list = []
    for i in range(n_vehicles):
        data_i = np.array(re.split(re.compile(' +'), data[i+1]))
        tmp = []
        for j in range(len(data_i)):
            tmp.append(float(data_i[j]))
        data_i = np.array(tmp)
        vehicle_list.append(Vehicle(i, data_i))

    
    return (n_vehicles, vehicle_list)


def load_city_from_text(file_name):
    '''
    Params: 
    file_name: đường dẫn tới file text

    định dạng file text: 
    line 1: số lượng thành phố n
    2n line tiếp theo: dòng đầu là tọa độ, dòng sau là demand đối với mỗi loại mặt hàng
    Return:
    n_city: số lượng thành phố
    city_list: list class City
    '''
    with open(file_name, 'r') as f:
        data = f.read()
    data = data.split('\n')

    n_cities = int(data[0])
    city_list = []
    for i in range(n_cities):

        location_i = np.array(re.split(re.compile(' +'), data[2*i+1]))
        demand_i = np.array(re.split(re.compile(' +'), data[2*i+2]))
        tmp = []
        for j in range(len(location_i)):
            tmp.append(float(location_i[j]))
        location_i = np.array(tmp)

        tmp = []
        for j in range(len(demand_i)):
            tmp.append(float(demand_i[j]))
        demand_i = np.array(tmp)
        city_list.append(Node(location_i[0], location_i[1], i, demand_i))
    
    return (n_cities, city_list)


def total_capacity(vehicle_list):
    '''
    Hàm tính tổng chuyên chở của các xe mỗi loại
    Input: list class Vehicle
    Output: mảng dài n_items
    '''
    n_vehicles = len(vehicle_list)
    total = np.zeros(len(vehicle_list[0].capacity_list))
    for vehicle in vehicle_list:
        total+=vehicle.capacity_list
    
    return total

def total_demand(city_list):
    '''
    Hàm tính tổng cần giao của các điểm mỗi loại
    Input: list class City
    Output: mảng dài n_items
    '''
    total = np.zeros(len(city_list[0].demand_array))
    for city in city_list:
        total+=city.demand_array
    
    return total

    