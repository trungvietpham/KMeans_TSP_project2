import numpy as np
from scipy.spatial import distance
import re
import sys
import json

from sklearn.utils import shuffle
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from SupportClass import Vehicle, Node, Cluster

def manhattan_distance(p1, p2):
    '''
    Params: nhận vào tọa độ 2 điểm
    Return: Khoảng cách giữa 2 điểm tính theo l1-norm
    '''
    return np.sum(np.abs(np.array(p1) - np.array(p2)))

def optimizer(city_list, cluster_list, alpha, penalty_coef, zero_penalty_coef):
    '''
    Dạng hàm: L1(city_i, center_j) - alpha*(chuyên chở - trọng số)

    Params:

    `city_list`: list class City

    `cluster_list`: list class Cluster

    `alpha`: trọng số của khối lượng trong công thức hàm tối ưu

    `penalty_coef`: hệ số phạt cho những item đã quá khối lượng cho phép

    `zero_penalty_coef`: hệ số phạt cho item không chở được, nên đặt là 1 số rất lớn (1000000)

    Return:

    Trả về dạng 1 mảng n_city hàng, n_clusters cột

    Trả về 1 mảng labels n_city hàng

    '''
    n_cities = len(city_list)
    n_clusters  = len(cluster_list)

    #Shuffle cities:
    shuffle_index = [i for i in range(n_cities)]
    shuffle_index = shuffle(shuffle_index)
    print(shuffle_index)
    city_list_shuffle = [city_list[i] for i in shuffle_index]
    # for i in range(n_cities): city_list_shuffle[i].print(id_flag = True)

    labels = np.zeros(n_cities)
    result_array = np.zeros((n_cities, n_clusters))
    for i in range(n_cities):
        city_id = city_list_shuffle[i].id
        for j in range(n_clusters):
            result_array[i,j] = manhattan_distance(city_list_shuffle[i].get_location(), cluster_list[j].get_center()) 

            remain_capa = np.array(cluster_list[j].capacity_list) - np.array(cluster_list[j].current_mass) - city_list_shuffle[i].demand_array
            tmp = 0.0
            for k in range(len(remain_capa)): 
                if remain_capa[k]>0: tmp+=remain_capa[k]
                elif cluster_list[j].capacity_list[k] == 0: tmp+=zero_penalty_coef*remain_capa[k]
                else: tmp+=penalty_coef*remain_capa[k]

            tmp = tmp/np.sum(np.array(cluster_list[j].capacity_list))
            result_array[i,j] -= alpha*tmp
            print('Res[{}, {}] = {}'.format(i,j,result_array[i,j]))

        labels[city_id] = np.argmin(result_array[i])
        # print('Assign to cluster {}'.format(labels[-1]))
        # print('Before assign: ')
        # for k in range(n_clusters):
        #     print('Cluster {}: '.format(k))
        #     cluster_list[k].print()
        (cluster_list[int(labels[city_id])]).update_mass(city_list_shuffle[i].demand_array, city_list_shuffle[i].id)
        city_list_shuffle[i].print(id_flag = True)
        city_list_shuffle[i].cluster_id = labels[city_id]

        print('After assign: ')
        for k in range(n_clusters): 
            print('Cluster {}: '.format(k))
            cluster_list[k].print()
    
    return (result_array, np.array(labels))

def load_vehicle_from_text(file_name, n_items):
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
        item_i = np.array(re.split(re.compile(' +'), data[2*i+1]))
        data_i = np.array(re.split(re.compile(' +'), data[2*i+2]))
        data_array_i = np.zeros(n_items)
        for j in range(len(item_i)):
            data_array_i[int(item_i[j])-1] = float(data_i[j])
        vehicle_list.append(Vehicle(i, data_array_i))

    
    return (n_vehicles, vehicle_list)


def load_node_from_text(file_name, format, n_items):
    '''

    Params: 

    file_name: đường dẫn tới file text

    format: phần nội dung sẽ đọc vào, nhận giá trị là 'market', 'vendor', 'depot'

    định dạng file text: 
    line 1: số lượng thành phố n
    2n line tiếp theo: dòng đầu là tọa độ, dòng sau là demand đối với mỗi loại mặt hàng
    Return:
    n_city: số lượng thành phố
    city_list: list class City
    '''

    if format not in ['market', 'vendor', 'depot']: 
        raise Exception("format must be in list 'market', 'vendor', 'depot'. Found {}".format(format))
    
    with open(file_name, 'r') as f:
        data = f.read()
    data = data.split('\n')

    offset = 0
    #Tìm ra vị trí bắt đầu đọc
    for line in data:
        offset += 1
        if format in line: break

    n_cities = int(data[0+offset])
    city_list = []
    for i in range(n_cities):

        location_i = np.array(re.split(re.compile(' +'), data[3*i+1 + offset]))
        index_i = np.array(re.split(re.compile(' +'), data[3*i+2 + offset]))
        demand_i = np.array(re.split(re.compile(' +'), data[3*i+3 + offset]))
        tmp = []
        for j in range(len(location_i)):
            tmp.append(float(location_i[j]))
        location_i = np.array(tmp)

        demand_list_i = np.zeros(n_items)
        for j in range(len(demand_i)):
            demand_list_i[int(index_i[j])-1] = float(demand_i[j])
        city_list.append(Node(location_i[0], location_i[1], i, demand_list_i))
    
    return (n_cities, city_list)

def load_item_from_text(file_name):
    '''
    Load danh sách các item từ file text
    
    Return: (n_items, item_list)
    '''
    with open(file_name, 'r') as f:
        data = f.read()
    data = data.split('\n')
    n_items = int(data[0])
    item_list = []
    for i in range(n_items):
        tmp = [data[2*i+1], data[2*i+2]]
        item_list.append(tmp)
    
    return (n_items, item_list)



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

def output_to_json_file(cluster_list, city_list, dump_file = 'output/phase2.json'):
    '''
    dạng json: 
    "": {
        id
        center: {
            x:
            y:
        }
        node_list:{
            "":{
                id:
                demand:{
                    item1:{
                        name:
                        quantity:
                        unit:
                    }
                }
            }
        }
    }
    '''
    save_data = {}
    n_cluster = len(cluster_list)
    n_city = len(city_list)
    for i in range(n_cluster):
        tmp = {}
        tmp['id'] = i
        center_tmp = {}

        center_tmp['x'] = cluster_list[i].x
        center_tmp['y'] = cluster_list[i].y
        tmp['center'] = center_tmp

        cities_tmp = {}
        for city_id in cluster_list[i].city_id_list:
            city_tmp = {}
            city_tmp['id'] = int(city_id)
            demand = city_list[int(city_id)].demand_array
            demand_tmp = {}
            for j in range(len(demand)):
                demand_tmp['Item ' + str(j)] = demand[j]
            
            city_tmp['demand'] = demand_tmp
            cities_tmp[str(int(city_id))] = city_tmp
        tmp['node_list'] = cities_tmp
        save_data[str(i)] = tmp
    
    with open(dump_file, 'w', encoding='utf-8') as json_file:
        json.dump(save_data, json_file, ensure_ascii=False, indent=4)

