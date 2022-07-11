from turtle import pen
import numpy as np 
import sys

from sklearn.utils import shuffle
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from KMeans import KMeans
from utils import *

print('Start model:')
item_fname = 'input/item.txt'
city_fname = 'input/node.txt'
vehicle_fname = 'input/vehicle.txt'

(n_items, item_list) = load_item_from_text(item_fname)
(n_cities, city_list) = load_node_from_text(city_fname, format='market', n_items=n_items)
(n_vehicles, vehicle_list) = load_vehicle_from_text(vehicle_fname, n_items=n_items)
print('\tPrepare for clustering:')

n_clusters = n_vehicles
print('Num of cities: {}\nNum of cluster: {}'.format(n_cities, n_clusters))
capa = total_capacity(vehicle_list)
demand = total_demand(city_list)
#Scaler: Số đại diện cho số chuyến đi của các shipper
scaler = np.ceil(np.max(demand/capa))
print('Total capacity = {}\nTotal demand =   {}'.format(capa, demand))
print('Scaler: {}'.format(scaler))

#capacity_array: mảng n_cluster * n_items là sức chứa của từng cluster với mỗi item
capacity_array = []
for i in range(n_clusters):
    capacity_array.append(scaler*vehicle_list[i].capacity_list)
capacity_array = np.array(capacity_array)

model = KMeans(n_clusters)
(centers, labels, it, cluster_list) = model.fit(optimizer, city_list, capacity_array, alpha=2, penalty_coef=6)
print('Coverged after {} step'.format(it))

#In ra các thông tin trong cụm:
for i in range(len(cluster_list)):
    print('Cluster {}: '.format(i))
    cluster_list[i].print(True, True, True, True,True, '\t')

output_to_json_file(cluster_list, city_list, 'output/phase2.json')



