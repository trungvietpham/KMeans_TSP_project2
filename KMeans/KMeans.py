from select import select
import numpy as np
from scipy import rand 
from scipy.spatial import distance

import sys
from sklearn import cluster

from utils.utils import manhattan_distance

sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils.SupportClass import Cluster

class KMeans:
    '''
    Xây dựng lại thuật toán KMeans nhưng sử dụng hàm tối ưu tự xây dựng
    pass vào n_clusters là số cụm cần chia
    '''
    def __init__(self, n_clusters:int):
        self.n_clusters = n_clusters

    
    def init_centers(self, city_list):
        '''
        Params: 
        city_array: list class City
        Return: List chứa tọa độ của các tâm
        '''
        index_list = np.random.choice(int(len(city_list)), self.n_clusters, replace=False)
        rand_city_list = []
        for i in index_list:
            rand_city_list.append(city_list[i])
        clusters_list = []
        
        for i in range(self.n_clusters): 
            clusters_list.append([rand_city_list[i].x, rand_city_list[i].y])
        return clusters_list

    def assign_labels(self, optimizer, city_list, cluster_list, distance_coef, alpha, penalty_coef, zero_penalty, normalization_flag, shuffle = False):
        '''
        Params: 
        optimizer: hàm tối ưu (tự build) - cần trả về dạng 1 mảng city_array hàng, centers cột
        city_list: list class City
        cluster_list: list class Cluster
        Return: Vector cột mà gồm id của từng điểm dữ liệu thuộc về
        '''
        (distance, labels) = optimizer(city_list, cluster_list, distance_coef, alpha, penalty_coef, zero_penalty, normalization_flag=normalization_flag, shuffle_flag = shuffle)
        # return index of the closest center
        return (distance, labels)

    def update_centers(self, city_list, labels, distance_coef):
        centers = np.zeros((self.n_clusters, 2))
        cities = []
        n_items = len(city_list[0].demand_array)
        distance_list = []
        #for k in range(self.n_clusters):
        for i in range(len(city_list)):
        # collect all points assigned to the k-th cluster 
            cities.append(city_list[i].get_location())
        
        # print(cities)
        # print(labels)
        for k in range(self.n_clusters):
            cities_k = []
            for i in range(len(labels)):
                if labels[i][1] == k: cities_k.append(cities[i])
                # take average
                #Note: Sửa lại để cập nhật theo hàm optimizer
            if len(cities_k) != 0: 
                centers[k,:] = np.mean(cities_k, axis = 0)
            dist = 0.0
            for a in cities_k:
                dist+=manhattan_distance(a, centers[k, :])
            distance_list.append(dist*distance_coef)
        return (distance_list, centers)


    def has_converged(self, centers, new_centers, epsilon = 1e-6):
        '''
        Params: 
        centers: Mảng chứa tọa độ các tâm cũ
        new_centers: Mảng chứa tọa độ các tâm mới
        epsilon: Ngưỡng để kiểm tra hội tụ

        Return: True nếu tâm cập nhật không quá epsilon
        '''
        
        diff: float
        diff = 0.0
        length = len(centers)
        for i in range(length): 
            # print('Cluster {}: Old center: {}, new center: {}'.format(i, centers[i], new_centers[i]))
            diff += distance.euclidean(centers[i], new_centers[i])
        
        diff/=self.n_clusters

        return diff<epsilon


    def fit(self, optimizer, city_list, capacity_array, distance_coef, epsilon = 1e-6, normalization_flag=True, alpha = 100, penalty_coef = 300, zeros_penalty = 100000, shuffle = False):
        '''
        Hàm fit để thực hiện quá trình học của thuật toán.

        Params: 

        optimizer: hàm tối ưu 

        city_list: list class City
        capacity_array: Mảng n_clusters * n_items là sức chuyên chở đối với mỗi mặt hàng của từng xe

        epsilon: Ngưỡng để kiểm tra hội tụ (điểm dừng của quá trình học)
        alpha: Trọng số của phần khối lượng trong công thức tối ưu
        penalty_coef: hệ số penalty

        Return:
        centers: list tọa độ các tâm cụm
        labels: list các nhãn của city sau mỗi bước
        it: số vòng lặp đến khi hội tụ
        '''
        # print('Fit thread')
        centers = [np.array(self.init_centers(city_list))]
        labels = []
        cluster_list = []
        # print('On start')
        for i in range(self.n_clusters):
            location = centers[-1][i]
            capacity_list = np.array(capacity_array[i])
            cluster_list.append(Cluster(location[0], location[1], capacity_list, city_id_list=[]))
            # print('Cluster {}, city list: {}'.format(i, cluster_list[-1].city_id_list))
        it = 0 
        continue_flag = True
        while continue_flag:
            # print('Loop thread')
            _, label = self.assign_labels(optimizer, city_list, cluster_list, distance_coef, alpha, penalty_coef, zeros_penalty, shuffle=shuffle, normalization_flag=True)
            labels.append(label)
            # print('Assign done')
            total_dis, new_centers = self.update_centers(city_list, labels[-1], distance_coef)
            # print('Update done')
            # for cluster_id in range(len(cluster_list)):
                # print('\tCluster {}: City list = {}'.format(cluster_id, cluster_list[cluster_id].city_id_list))
            if self.has_converged(centers[-1], new_centers, epsilon):
                # print('Coverged!!!!')
                continue_flag = False
                break
            centers.append(new_centers)
            for i in range(self.n_clusters):
                # print('Set lại tâm cụm')
                cluster_list[i].set_center(centers[-1][i])
                # print('\tTâm cụm {} mới: {}'.format(i, cluster_list[i].get_center()))
                cluster_list[i].clear_mass()
                #cluster_list[i].clear_city()
                # print('it = {}'.format(it))
            
            # print('it = {}'.format(it))
            it += 1
        return (centers, labels, it, cluster_list, total_dis)

    
        