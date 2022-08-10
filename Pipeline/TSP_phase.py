from ast import dump
from distutils.command.config import dump_file
from math import dist
from time import time
import numpy as np
import json
from python_tsp.exact import solve_tsp_dynamic_programming

import sys
import os
sys.path.append(os.getcwd())
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
    return (np.argmin(distance), np.min(distance))



def TSP_phase():
    #Load correlation 
    correlation = json.load(open('input/correlation.json', 'r'))
    cluster_data = json.load(open('output/pre_TSP_phase.json', 'r'))
    depot_data = json.load(codecs.open('input/depot.json', 'r', 'utf-8-sig'))
    dump_file = 'output/TSP_phase_with_Kmeans.json'

    summary = []
    details = []
    details.append('\nDescription: Use TSP algorithm for each sub-cluster\n')

    details.append('\tInput data list:')
    details.append('\t\tinput/correlation.json')
    details.append('\t\tinput/depot.json')
    details.append('\t\toutput/pre_TSP_phase.json')
    details.append('\tOutput data to: ')
    details.append('\t\t{}'.format(dump_file))

    #Lấy ra toàn bộ tọa độ của các depot và lưu vào list
    depot_list = []
    for depot_key in depot_data['depot']:
        depot_list.append([depot_data['depot'][depot_key]['location']['lat'], depot_data['depot'][depot_key]['location']['long']])
    del depot_key

    # Dict lưu lại các thông tin để lưu trữ
    save_data = {}

    # Một số biến lưu trữ tổng độ dài TSP, thời gian tính toán
    route_distance = []
    time_computing = []
    route_list = []

    #Lặp qua các cụm con và tsp 
    for cluster_parent_key in cluster_data:
        center_parent = cluster_data[cluster_parent_key]['center']
        n_cluster_child = len(cluster_data[cluster_parent_key]["child_cluster_list"])
        cluster_info = {}
        cluster_info['cluster_id'] = cluster_parent_key
        cluster_info['center'] = cluster_data[cluster_parent_key]['center']
        cluster_info["child_cluster_list"] ={}

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
                    if mapping[j] not in correlation[mapping[i]]: correlation[mapping[i]][mapping[j]] = 0.0 
                    distance_matrix[i][j] = correlation[mapping[i]][mapping[j]]
            
            #TSP
            time1 = time()
            permutation, _ = solve_tsp_dynamic_programming(distance_matrix)
            time2 = time()

            reverse_permutation = []
            for i in range(n_node_child+1):
                reverse_permutation.append(mapping[int(permutation[i])])
            # reverse_permutation.append(mapping[int(permutation[0])])
            # print('Cluster cha = {}, cluster con = {}'.format(cluster_parent_key, cluster_child_key))
            # print('Permutation: {}'.format(' -> '.join(reverse_permutation)))
            # print('Distance = {}'.format(dist_res))

            dist_res = 0.0
            for i in range(1, len(reverse_permutation)):
                dist_res += float(correlation[reverse_permutation[i-1]][reverse_permutation[i]]/1000)

            dist_res = round(dist_res, 0)
            route_list.append(' -> '.join(reverse_permutation))
            cluster_info["child_cluster_list"][cluster_child_key] = {}
            cluster_info["child_cluster_list"][cluster_child_key]['route']= ' -> '.join(reverse_permutation)
            cluster_info["child_cluster_list"][cluster_child_key]['length'] = str(round(dist_res, 0)) + ' km'

            # Lưu lại các thông tin về khoảng cách, thời gian tính toán
            route_distance.append(dist_res)
            time_computing.append(time2-time1)
            #Xóa bộ nhớ
            del cluster_child, mapping, reverse



        save_data[cluster_parent_key] = cluster_info

    #Dump ra file 'output/TSP_phase.json'
    json.dump(save_data, open(dump_file, 'w'), indent=4)

    summary_for_compare = {'Distance': np.sum(np.array(route_distance)), 'Time': round(np.sum(np.array(time_computing))*1000.0, 0)}
    json.dump(summary_for_compare, open('output/summary_TSP_with_Kmeans.json', 'w'), indent=4)


    print('\tSummary: ')
    print('\t\tTotal route length = {} (km)'.format(np.sum(np.array(route_distance))))
    print('\t\tTotal time computing TSP = {} ms'.format(round(np.sum(np.array(time_computing))*1000.0, 0)))

    summary.append('\tSummary: ')
    summary.append('\t\tTotal route length = {} (km)'.format(np.sum(np.array(route_distance))))
    summary.append('\t\tTotal time computing TSP = {} ms'.format(round(np.sum(np.array(time_computing))*1000.0, 0)))

    details.append('\n'.join(summary))
    details.append('\tDetails: ')

    cnt = 0

    for cluster_parent_key in cluster_data:
        details.append('\t\tCluster parent: {}'. format(cluster_parent_key))
        for cluster_child_key in cluster_data[cluster_parent_key]["child_cluster_list"]:
            details.append('\t\t\tCLuster child: {}'.format(cluster_child_key))
            details.append('\t\t\tRoute: {}'.format(route_list[cnt]))
            details.append('\t\t\tTSP route length: {} (km)'.format(route_distance[cnt]))
            details.append('\t\t\tTime computing TSP: {}'.format(round(time_computing[cnt]*1000.0, 0)))
            cnt+=1
    
    details.append('\n\n')
    summary.append('\n\n')
    return ('\n'.join(summary), '\n'.join(details), dump_file, np.sum(np.array(route_distance)), round(np.sum(np.array(time_computing))*1000.0, 0))
    # Return (string summary, string details, outter file, total distance in km, total time in ms)

if __name__ == "__main__":
    TSP_phase()


