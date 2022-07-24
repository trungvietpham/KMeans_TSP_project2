from turtle import pen
import numpy as np 
import sys

from sklearn.utils import shuffle
import os
sys.path.append(os.getcwd())
from KMeans.KMeans import KMeans
from utils.utils import *

print('Start model:')
item_fname = 'input/item.txt'
#city_fname = 'input/node.txt'
city_fname = 'input/market.json'
vehicle_fname = 'input/vehicle.json'
convert_coef_fname = 'input/latlong_to_meter_coef.txt'

(n_items, item_list) = load_item_from_text(item_fname)
#(n_cities, city_list) = load_node_from_text(city_fname, format='market', n_items=n_items)
(n_cities, city_list) = load_node_from_json(city_fname, format='market', n_items=n_items)
(n_vehicles, vehicle_list) = load_vehicle_from_json(vehicle_fname, n_items=n_items)
convert_coef = get_convert_coef_from_file(convert_coef_fname)
# print(vehicle_list)
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

(centers, labels, it, cluster_list) = model.fit(optimizer=optimizer, city_list = city_list,capacity_array = capacity_array, distance_coef=convert_coef, normalization_flag=False, alpha=200, penalty_coef=60000, zeros_penalty=10000000, shuffle=True, epsilon=1e-3)
print('Coverged after {} step'.format(it))

#In ra các thông tin trong cụm:
for i in range(len(cluster_list)):
    print('Cluster {}: '.format(i))
    cluster_list[i].print(True, True, True, True,True, '\t')

output_to_json_file(cluster_list, city_list, 'output/KMeans_phase.json')

'''
Save centers, labels, it thành dict và dump vào file json
Dạng file json: 
{
    'it': it
    'center':{
        it_number:{
            center_i: {
                'lat': x
                'long': y
            }
        }
    }
    'label':{
        it_number: {
            label_i: label
        }
    }
}
'''
# save_data = {}
# save_data['it'] = it
# centers_dict = {}
# labels_dict = {}
# label_0 = {}

# #Centers: 
# for i in range(it+1):
#     center_i = {}
#     for j in range(len(centers[i])):
#         center_i[str(j)] = {'lat':centers[i][j][0], 'long':centers[i][j][1]}
#     centers_dict[str(i)] = center_i

# #Label ban đầu đều là -1, tương ứng với nó là chưa được gán giá trị
# for j in range(len(labels[0])): label_0[str(j)] = -1
# labels_dict['0'] = label_0

# for i in range(it):
#     label_i = {}
#     for j in range(len(labels[i])):
#         label_i[str(j)] = labels[i][j]
#     labels_dict[str(i+1)] = label_i
# save_data['centers'] = centers_dict
# save_data['labels'] = labels_dict

# print('labels: {}\ncenters: {}'.format(labels, centers))
# f = open('output/for_plotting_phase2.json', 'w')
# json.dump(save_data, f, indent=4)

