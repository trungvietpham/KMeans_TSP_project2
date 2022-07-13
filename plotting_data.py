from tabnanny import check
import matplotlib.pyplot as plt
import numpy as np
import json 
import random

import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")

#Read data from phase2.json
fname = 'output/phase2_300.json'
f = open(fname, 'r')
data = json.load(f)

#Get n_clusters
n_clusters = len(data)

color_list = ['r', 'g', 'b','c', 'm', 'y', 'k', 'orange']
marker_list = ['.', 'v', '1', '8', 's','p', 'P', '*','+','x']
check_list = {}
n_colors = len(color_list)
n_markers = len(marker_list)

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
    
    plt.scatter(latitude, longtitude, c=color, marker=marker)
    plt.scatter(center_location['lat'], center_location['long'], c = 'red', marker='o', s=50)

plt.show()