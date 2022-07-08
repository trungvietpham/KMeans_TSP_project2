from turtle import pen
import numpy as np 
import sys

from sklearn.utils import shuffle
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from KMeans import KMeans
from utils import *

print('Start model:')
city_fname = 'VietVRP/data/city.txt'
vehicle_fname = 'VietVRP/data/vehicle.txt'

(n_cities, city_list) = load_city_from_text('VietVRP/data/city.txt')
(n_vehicles, vehicle_list) = load_vehicle_from_text('VietVRP/data/vehicle.txt')
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
(centers, labels, it) = model.fit(optimizer, city_list, capacity_array, alpha=2, penalty_coef=6)
print('Coverged after {} step'.format(it))



