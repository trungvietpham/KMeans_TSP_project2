import json
import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils.utils import *

n_items = 2
data = json.load(open('output/pre_TSP_phase.json', 'r'))
[n_vehicles, vehicle_list] = load_vehicle_from_json('input/vehicle.json', n_items)

cnt = 0
n_node_threshold = 15
for key1 in data:
    capa = np.array(vehicle_list[cnt].capacity_list) 
    for key2 in data[key1]["child_cluster_list"]:
        demand12 = np.zeros(n_items)
        for key3 in data[key1]["child_cluster_list"][key2]["node_list"]:
            demand12[0]+=float(data[key1]["child_cluster_list"][key2]["node_list"][key3]["demand"]['Item 0'])
            demand12[1] += float(data[key1]["child_cluster_list"][key2]["node_list"][key3]["demand"]['Item 1'])
        
        #Check current_mass nhỏ hơn capacity
        if not is_bigger_than(capa, demand12): print('Parent: {}, child: {}'.format(key1, key2))

        #Check n_cities < n_node_threshold
        if len(data[key1]["child_cluster_list"][key2]["node_list"]) > n_node_threshold: print('Parent: {}, child: {}'.format(key1, key2))
    cnt+=1
                
        