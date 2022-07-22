from math import dist
import numpy as np
import json
from python_tsp.exact import solve_tsp_dynamic_programming

import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils.utils import *

def get_nearest_depot(point, depot_list):
    '''
    point = [lat, long]: là tọa độ của tâm cụm
    depot_list = [[lat, long]]*n_depots
    Tính khoảng cách manhattan giữa point đối với từng điểm depot và
    lấy ra tọa độ của depot gần nhất đối với point
    '''
    depot_list = np.array(depot_list)
    distance = np.zeros(len(depot_list))
    for i in range(len(depot_list)):
        distance[i] = manhattan_distance(point, depot_list[i])
    return (np.argmax(distance), np.max(distance))



#Load correlation 
correlation = json.load(open('input/correlation.json', 'r'))

cluster_data = json.load(open('output/pre_TSP_phase.json', 'r'))

depot_data = json.load(codecs.open('input/depot.json', 'r', 'utf-8-sig'))

#Lấy ra toàn bộ tọa độ của các depot và lưu vào list
depot_list = []
for depot_key in depot_data['depot']:
    depot_list.append([depot_data['depot'][depot_key]['location']['lat'], depot_data['depot'][depot_key]['location']['long']])
del depot_key

#Lặp qua các cụm con và tsp 
for cluster_parent_key in cluster_data:
    center_parent = cluster_data[cluster_parent_key]['center']
    n_cluster_child = len(cluster_data[cluster_parent_key]["child_cluster_list"])

    for cluster_child_key in cluster_data[cluster_parent_key]["child_cluster_list"]:
        cluster_child = cluster_data[cluster_parent_key]["child_cluster_list"][cluster_child_key]
        (index, dis) = get_nearest_depot(point=(cluster_child["center"]['lat'], cluster_child["center"]['long']), depot_list=depot_list)
        n_node_child = len(cluster_child["node_list"])
        node_id_list = ['D'+str(index)] #Lưu lại các node có trong cluster con này

        #Mapping từ số trong khoảng (0, n_node_child) về id node 
        mapping = {0:'D'+str(index)}
        reverse = {'D'+str(index):0}
        cnt = 1
        for id in cluster_child['node_list']:
            mapping[cnt] = 'C' + str(id)
            reverse['C' + str(id)] = cnt
            node_id_list.append('C'+str(id))
            cnt+=1
        del cnt

        # Tạo 1 mảng 2 chiều là distance giữa 2 node bất kỳ trong đây, 
        distance_matrix = np.zeros((n_node_child+1, n_node_child+1))
        for i in range(n_node_child+1):
            for j in range(n_node_child+1):
                distance_matrix[i][j] = correlation[mapping[i]][mapping[j]]
        
        #TSP
        permutation, dist_res = solve_tsp_dynamic_programming(distance_matrix)

        reverse_permutation = []
        for i in range(n_node_child+1):
            reverse_permutation.append(mapping[int(permutation[i])])
        print('permutation: {}'.format('-->'.join(reverse_permutation)))
        print('Distance = {}'.format(dist_res))
        exit(0)


