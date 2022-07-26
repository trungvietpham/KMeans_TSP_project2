from tabnanny import check
import matplotlib.pyplot as plt
import numpy as np
import json 
import random

import sys
import os
sys.path.append(os.getcwd())

def plotting_for_phase1():
    #Read data from phase2.json
    fname = 'output/KMeans_phase.json'
    f = open(fname, 'r')
    data = json.load(f)

    #Get n_clusters
    n_clusters = len(data)

    color_list = ['g', 'b','c', 'm', 'y', 'k', 'orange']
    marker_list = ['.', 'v', '1', '8', 's','p', 'P', '*','+','x']
    check_list = {}
    n_colors = len(color_list)
    n_markers = len(marker_list)

    a = plt.figure(1)

    for cluster_index in range(n_clusters):
        clusters_i = data[str(cluster_index)]
        center_location = clusters_i['center']
        latitude = []
        longtitude = []
        for city_key in clusters_i['node_list']:
            latitude.append(clusters_i['node_list'][city_key]['node_location']['lat'])
            longtitude.append(clusters_i['node_list'][city_key]['node_location']['long'])
        
        #Chọn màu và marker cho cluster:
        while True:
            color = color_list[random.randint(0, n_colors-1)]
            marker = marker_list[random.randint(0, n_markers-1)]
            pair_check = color+marker
            if pair_check not in check_list:
                check_list[pair_check] = 1
                break
        
        plt.scatter(latitude, longtitude, c=color, marker=marker, s=15)
        plt.scatter(center_location['lat'], center_location['long'], c = 'red', marker='o', s=25)

    # plt.show()
    return a

def plotting_for_pre_phase2():
    fname = 'output/pre_TSP_phase.json'
    f = open(fname, 'r')
    data = json.load(f)

    #Get n_clusters
    n_clusters = len(data)

    color_list = ['g', 'b','c', 'm', 'y', 'k', 'orange']
    marker_list = ['.', 'v', '1', '8', 's','p', 'P', '*','+','x']
    
    n_colors = len(color_list)
    n_markers = len(marker_list)

    b = plt.figure(2)

    for cluster_index in range(n_clusters):
        check_list = {}
        clusters_i = data[str(cluster_index)]
        center_location = clusters_i['center']
        for child_cluster_index in clusters_i["child_cluster_list"]:
            latitude = []
            longtitude = []
            center_child = clusters_i["child_cluster_list"][child_cluster_index]['center']
            for city_key in clusters_i["child_cluster_list"][child_cluster_index]['node_list']:
                latitude.append(clusters_i["child_cluster_list"][child_cluster_index]['node_list'][city_key]['node_location']['lat'])
                longtitude.append(clusters_i["child_cluster_list"][child_cluster_index]['node_list'][city_key]['node_location']['long'])
            
            #Chọn màu và marker cho cluster:
            while True:
                color = color_list[random.randint(0, n_colors-1)]
                marker = marker_list[random.randint(0, n_markers-1)]
                pair_check = color+marker
                if pair_check not in check_list:
                    check_list[pair_check] = 1
                    break
            
            x_values = [center_location['lat'], center_child['lat']]
            y_values = [center_location['long'], center_child['long']]
            plt.plot(x_values, y_values, 'bo', linestyle="--", markersize=2, linewidth=1)
            plt.scatter(latitude, longtitude, c=color, marker=marker, s=15)
            plt.scatter(center_child['lat'], center_child['long'], c = 'red', marker='o', s=25)
        
        plt.scatter(center_location['lat'], center_location['long'], c='red', marker='o', s = 30)

    # plt.show()
    return b

# a = plotting_for_pre_phase2()
b = plotting_for_phase1()

plt.show()
# a.show()
b.show()
# input()