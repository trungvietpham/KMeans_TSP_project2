'''
Cắt cụm to ra thành các cụm con để sử dụng thuật toán TSP
1. Đọc các dữ liệu từ output phase 1 vào và các dữ liệu về xe, items, ...
2. KMeans để chia ra 1 cụm thành các cụm con có thể di chuyển trong 1 route
3. Dump lại các cụm con ra 1 file json
'''

from time import time
import numpy as np
import json
import sys
from sklearn.covariance import oas

from sklearn.utils import shuffle
import os
sys.path.append(os.getcwd())
from KMeans.KMeans import KMeans
from utils.utils import *

def Pre_TSP_phase(n_node_threshold = 15):
    item_fname = 'input/item.txt'
    city_fname = 'input/market.json'
    vehicle_fname = 'input/vehicle.json'
    convert_coef_fname = 'input/latlong_to_meter_coef.txt'
    output_phase1_fname = 'output/KMeans_phase.json'

    (n_items, item_list) = load_item_from_text(item_fname)
    (n_cities, city_list) = load_node_from_json(city_fname, format='market', n_items=n_items)
    (n_vehicles, vehicle_list) = load_vehicle_from_json(vehicle_fname, n_items=n_items)
    convert_coef = get_convert_coef_from_file(convert_coef_fname)
    cluster_data = json.load(open(output_phase1_fname, 'r'))
    n_clusters = len(cluster_data)

    '''
    1. Khôi phục lại các cụm từ output_phase1_file
    '''
    cluster_list = []
    cnt = 0
    for cluster_id in cluster_data:
        x, y = cluster_data[cluster_id]['center']['lat'], cluster_data[cluster_id]['center']['long']
        n_cities_i = len(cluster_data[cluster_id]['node_list'])
        child_list = []
        mass = np.zeros(n_items)

        for id in cluster_data[cluster_id]['node_list']:
            child_list.append(int(id))
            for i in range(n_items):
                mass[i]+=cluster_data[cluster_id]['node_list'][id]["demand"]['Item '+str(i)]
        cluster_list.append(Cluster(x,y,None, n_cities=n_cities_i, city_id_list=child_list, current_mass=mass))
        # print('Cluster {}: \n\tChild list = {}\n\tCurrent mass = {}'.format(cnt, child_list, mass))
        # child_list = None
        # cnt+=1

    '''
    2. Với mỗi cụm ta chia thành các cụm nhỏ, số lượng cụm nằm trong khoảng [max(ceil(tổng/capa)), n_node/(floor(min(capa/mean)))]
    Số node trong cụm được giới hạn bởi 1 biến, đặt = 15
    '''

    # Một số biến lưu trữ các thông tin về số lần thử kmeans, số cụm cha, số cụm con
    try_kmeans_counter = 0
    n_cluster_parent = 0
    n_cluster_child = []
    total_distance = []
    time_computing = []

    low_n_cluster = []
    for i in range(n_clusters):

        #Lấy ra chặn dưới sổ lượng cụm
        low_n_cluster.append(int(np.ceil(np.max(cluster_list[i].current_mass/np.array(vehicle_list[i].capacity_list)))))
        
    #Với cụm thứ i, low_n_cluster[i] là chặn dưới số cụm con được phân ra từ cụm cha đó
    #Tiến hành chia cụm và sau đó lưu vào 1 dict để dump vào file
    save_data = {}
    for cluster_id in range(n_clusters):
        n_cluster_parent +=1
        n_child = low_n_cluster[cluster_id]

        #Lấy ra các node nằm trong cluster cha này
        child_city_list = []
        child_id = []
        child_id = sorted(cluster_list[cluster_id].city_id_list)
        # print('Cluster {}: \n\tChild list = {}'.format(cluster_id, child_id))
        for city in child_id:
            child_city_list.append(city_list[city])
        
        # Bắt đầu lặp từ giá trị n_child, mỗi khi phân cụm xong, ta kiểm tra xem 
        # các current_mass có đều nhỏ hơn capacity của xe hay không, nếu không thì ta tăng giá trị n_child và lặp lại
        continue_flag = True
        time1 = time()
        while continue_flag:
            
            capacity_array = np.array([list(vehicle_list[cluster_id].capacity_list)]*n_child).reshape((n_child, n_items))
            model = KMeans(n_child)
            # print('Cluster {}'.format(cluster_id))
            (_,_,_, child_cluster_list, distance) = model.fit(optimizer=optimizer, city_list = child_city_list,capacity_array = capacity_array, distance_coef=convert_coef, normalization_flag=False, alpha=500, penalty_coef=100000, zeros_penalty=10000000, shuffle=True, epsilon=1e-3)
            
            continue_flag = False
            for child in child_cluster_list:
                #Kiểm tra nếu current_mass của cụm lớn hơn capacity của xe thì set flag thành true
                if not is_bigger_than(child.capacity_list, child.current_mass): 
                    continue_flag = True
                    # print('capa = {}, current mass = {}'.format(child.capacity_list, child.current_mass))
                    # input("Press Enter to continue...")
                    break

                #Kiểm tra nếu số node lớn hơn n_node_threshold thì set flag thành true
                if child.n_cities > n_node_threshold:
                    continue_flag = True
                    break
            
            if continue_flag == True: 
                n_child+=1
                try_kmeans_counter+=1
                del child_cluster_list
                del model
                del capacity_array
            else: 
                # for child in child_cluster_list:
                    # print('Current mass = {}, Child list = {} '.format(child.current_mass, child.city_id_list))
                # print('Cluster {}: \n\tChild list = {}\n\tCurrent mass = {}'.format(cluster_id, child_list, mass))
                
                time2 = time()

                cluster_parent_info = {}
                cluster_parent_info['cluster_id'] = cluster_id
                cluster_parent_info['center'] = cluster_data[str(cluster_id)]['center']

                cluster_children_info = output_to_json_file(child_cluster_list, child_city_list, output_flag=False)

                cluster_parent_info['child_cluster_list'] = cluster_children_info
                save_data[cluster_id] = cluster_parent_info

                # Update các thông tin để in ra màn hình
                n_cluster_child.append(n_child)
                total_distance.append(distance)
                time_computing.append(time2-time1)


    '''
    3. Dump ra file json, lấy tên là pre_TSP_phase.json
    '''
    dump_file = 'output/pre_TSP_phase.json'
    with open(dump_file, 'w', encoding='utf-8') as json_file:
        json.dump(save_data, json_file, ensure_ascii=False, indent=4)

        #TODO: lấy ra các thành phố thuộc vào cụm cha này, sau đó fit vào model, lưu lại các thông tin về nhãn của từng cụm con để biểu diễn dữ liệu

    print('\tSummary: ')
    print('\t\tTotal try KMeans times = {}'.format(try_kmeans_counter))
    print('\t\tNo. cluster parent = {}'.format(n_cluster_parent))
    print('\t\tNo. cluster child = {}'.format(np.sum(np.array(n_cluster_child))))
    print('\t\tTotal distance = {} (m)'.format(round(np.sum(np.array(total_distance)), 3)))
    print('\t\tTotal time for clustering = {} ms'.format(round(np.sum(np.array(time_computing))*1000.0, 3)))

# Pre_TSP_phase()