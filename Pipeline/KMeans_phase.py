import time
from turtle import pen
import numpy as np 
import sys
from sklearn import cluster

from sklearn.utils import shuffle
import os
sys.path.append(os.getcwd())
from KMeans.KMeans import KMeans
from utils.utils import *

def KMeans_phase(vehicle_fname):
    # print('Start model:')
    item_fname = 'input/item.txt'
    #city_fname = 'input/node.txt'
    city_fname = 'input/market.json'
    convert_coef_fname = 'input/latlong_to_meter_coef.txt'

    (n_items, item_list) = load_item_from_text(item_fname)
    #(n_cities, city_list) = load_node_from_text(city_fname, format='market', n_items=n_items)
    (n_cities, city_list) = load_node_from_json(city_fname, format='market', n_items=n_items)
    (n_vehicles, vehicle_list) = load_vehicle_from_json(vehicle_fname, n_items=n_items)
    convert_coef = get_convert_coef_from_file(convert_coef_fname)
    # print(vehicle_list)
    # print('\tPrepare for clustering:')

    n_clusters = n_vehicles
    # print('Num of cities: {}\nNum of cluster: {}'.format(n_cities, n_clusters))
    capa = total_capacity(vehicle_list)
    demand = total_demand(city_list)
    #Scaler: Số đại diện cho số chuyến đi của các shipper
    scaler = np.ceil(np.max(demand/capa))
    # print('Total capacity = {}\nTotal demand =   {}'.format(capa, demand))
    # print('Scaler: {}'.format(scaler))

    #capacity_array: mảng n_cluster * n_items là sức chứa của từng cluster với mỗi item
    capacity_array = []
    for i in range(n_clusters):
        capacity_array.append(scaler*vehicle_list[i].capacity_list)
    capacity_array = np.array(capacity_array)

    model = KMeans(n_clusters)

    time1 = time.time()
    (centers, labels, it, cluster_list, total_distance) = model.fit(optimizer=optimizer, city_list = city_list,capacity_array = capacity_array, distance_coef=convert_coef, normalization_flag=False, alpha=200, penalty_coef=60000, zeros_penalty=10000000, shuffle=True, epsilon=1e-3)
    time2 = time.time()

    total_mass = np.zeros(n_items)
    for cluster in cluster_list:
        total_mass += np.array(cluster.current_mass)

    print('\tSummary: ')
    print('\t\tConverged after {} steps'.format(it))
    print('\t\tNo. of clusters = No. of vehicles = {}'.format(len(cluster_list)))
    print('\t\tNo. of customers = {}'.format(len(labels[-1])))
    print('\t\tNo. of good types =  {}'.format(n_items))
    print('\t\tTotal picked capacity = {} kg'.format(total_mass))
    print('\t\tTotal delivered capacity = {} kg'.format(total_mass))
    print('\t\tTotal distance = {} (km)'.format(round(np.sum(total_distance), 3)))
    print('\t\tClustering duration = {} ms'.format(round((time2-time1)*1000.0, 0)))

    output_to_json_file(cluster_list, city_list, 'output/KMeans_phase.json')

    summary = []
    details = []
    summary.append('\tSummary: ')
    summary.append('\t\tConverged after {} steps'.format(it))
    summary.append('\t\tNo. of clusters = No. of vehicles = {}'.format(len(cluster_list)))
    summary.append('\t\tNo. of customers = {}'.format(len(labels[-1])))
    summary.append('\t\tNo. of good types =  {}'.format(n_items))
    summary.append('\t\tTotal picked capacity = {} kg'.format(total_mass))
    summary.append('\t\tTotal delivered capacity = {} kg'.format(total_mass))
    summary.append('\t\tTotal distance = {} (km)'.format(round(np.sum(total_distance), 3)))
    summary.append('\t\tClustering duration = {} ms'.format(round((time2-time1)*1000.0, 0)))

    details.append('Description: Clustering {} customers into {} cluster ({} is no. of vehicles) by using KMeans clustering.\n'.format(n_cities, n_clusters, n_vehicles))
    details.append('\tInput data list:')
    details.append('\t\tinput/item.txt')
    details.append('\t\tinput/market.json')
    details.append('\t\tinput/latlong_to_meter_coef.txt')
    details.append('\tOutput data to:')
    details.append('\t\toutput/KMeans_phase.json')
    details.append('\t\t{}'.format(vehicle_fname))
    details.append('\n'.join(summary))
    details.append('\tDetails:')
    details.append('\t\tNo. items: {}'.format(n_items))

    for i in range(len(cluster_list)):
        details.append('\t\tCluster {}:'.format(i))
        details.append('\t\t\tCurrent mass = {}'.format(cluster_list[i].current_mass))
        details.append('\t\t\tNo. of customers = {}'.format(cluster_list[i].n_cities))
        details.append('\t\t\tDistance = {} (km)'.format(round(total_distance[i], 3)))
    details.append('\n\n')
    summary.append('\n\n')
    return ('\n'.join(summary), '\n'.join(details))