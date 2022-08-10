from ast import dump
import codecs
from distutils.command.config import dump_file
from math import dist
import random
from time import time
from tracemalloc import start
import numpy as np
import json
from python_tsp.exact import solve_tsp_dynamic_programming

import sys
import os

sys.path.append(os.getcwd())
from utils.utils import *


def get_nearest_node(start_node, length_matrix, type = 'C'):
    dis = 1e9
    index = None
    for element in length_matrix:
        if element[0] == type and dis>length_matrix[element] and length_matrix[element]>0:
            dis = length_matrix[element]
            index = int(element[1:])
    
    return (index, dis/1000)



def TSP_no_Kmeans(n_vehicle = 20):
    # Load các thông tin về vehicle, depot, correlation
    correlation = json.load(open('input/correlation.json', 'r'))
    depot_data = json.load(codecs.open('input/depot.json', 'r', 'utf-8-sig'))
    dump_file = 'output/TSP_no_KMeans.json'

    (n_items, item_list) = load_item_from_text('input/item.txt')
    #(n_cities, city_list) = load_node_from_text(city_fname, format='market', n_items=n_items)
    (n_cities, city_list) = load_node_from_json('input/market.json', format='market', n_items=n_items)
    (n_vehicles, vehicle_list) = load_vehicle_from_json('input/vehicle_{}.json'.format(n_vehicle), n_items=n_items)
    convert_coef = get_convert_coef_from_file('input/latlong_to_meter_coef.txt')

    save_data = {i: {} for i in range(n_vehicle)}


    remain_node_index = [i for i in range(n_cities)]

    continue_flag = True # Cờ cho vòng while
    n_route_current = 0
    n_point = []
    length_list = []

    time1 = []
    time2 = []

    while continue_flag:
        continue_flag = False
        for v_index in range(n_vehicle):
            if len(remain_node_index) == 0: break
            current_mass = np.zeros(n_items)

            next_vehicle_flag = True
            time1.append(time())
            for _ in range(5): # Thử 5 lần sinh số, nếu đều không thỏa mãn thì coi như không còn node nào thỏa mãn, chuyển qua xe khác
                gen_num = random.randint(0, len(remain_node_index)-1)
                if is_bigger_than(vehicle_list[v_index].capacity_list, current_mass + np.array(city_list[remain_node_index[gen_num]].demand_array)):
                    next_vehicle_flag = False
                    break
            time2.append(time())

            if next_vehicle_flag == False:
                route = []
                length = 0.0

                time1.append(time())

                # # Remove phần tử ra khỏi các mảng và dict
                # del(correlation['C' + str(remain_node_index[gen_num])])
                # for key in correlation:
                #     del(correlation[key]['C' + str(remain_node_index[gen_num])])
                # remain_node_index.remove(remain_node_index[gen_num])
                current_mass += np.array(city_list[remain_node_index[gen_num]].demand_array)
                start_node = remain_node_index[gen_num]

                # Tìm depot gần nhất
                depot, _ = get_nearest_node('C'+str(start_node), correlation['C'+str(start_node)], 'D')
                route.append('D'+str(depot))
                length += float(correlation['D'+str(depot)]['C'+str(start_node)])/1000 # in km
                route.append('C' + str(start_node))

                

                a_flag = True # Cờ để chạy vòng lặp while dưới đây, false khi node gần nhất cộng vào vượt quá capacity của xe
                while a_flag: 
                    a_flag = False
                    start_node = int(route[-1][1:])
                    end_node, dis = get_nearest_node('C'+str(start_node), correlation['C'+str(start_node)], 'C')
                    if end_node is None: 
                        break
                    if is_bigger_than(vehicle_list[v_index].capacity_list, current_mass + np.array(city_list[end_node].demand_array)):
                        a_flag = True

                        current_mass+=np.array(city_list[end_node].demand_array)
                        route.append('C' + str(end_node))
                        length+=dis
                        # print('From {} to {}, v_index = {}'.format('C' + str(start_node), 'C' + str(end_node), v_index))
                        # start_node = end_node.copy()

                        
                        # Xóa đi các giá trị của start node
                        del(correlation['C' + str(start_node)])
                        for key in correlation:
                            del(correlation[key]['C' + str(start_node)])
                        remain_node_index.remove(start_node)

                
                # Xóa đi các giá trị của start node
                del(correlation['C' + str(start_node)])
                for key in correlation:
                    del(correlation[key]['C' + str(start_node)])
                remain_node_index.remove(start_node)
                
                time2.append(time())

                if len(route) != 0:
                    length = round(length)
                    save_data[v_index][n_route_current] = {}
                    save_data[v_index][n_route_current]['route'] = ' -> '.join(route)
                    save_data[v_index][n_route_current]['length'] = str(length) + ' km'
                    n_point.append(len(route)-1)
                    length_list.append(length)
                    # print('V_index = {}, n_points = {}'.format(v_index, n_point[-1]))
            
            if len(remain_node_index) != 0: continue_flag = True

    json.dump(save_data, open(dump_file, 'w'), indent=4)

    summary_for_compare = {'Distance': float(np.sum(np.array(length_list))), 'Time': float(round(np.sum(np.array(time2) - np.array(time1))*1000, 0))}
    json.dump(summary_for_compare, open('output/summary_TSP_no_Kmeans.json', 'w'), indent=4)

    print('Total length = {} (km)'.format(np.sum(np.array(length_list))))
    print('Total time = {} ms'.format(round(np.sum(np.array(time2) - np.array(time1))*1000, 0)))

    return (dump_file, np.sum(length_list), round(np.sum(np.array(time2) - np.array(time1))*1000, 0)) # outter file, total length in km, total time in ms


if __name__ == "__main__":
    TSP_no_Kmeans()
