from sklearn.utils import shuffle

import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils import load_city_from_text, load_vehicle_from_text, total_capacity, total_demand


(n_cities, city_list) = load_city_from_text('VietVRP/data/city.txt')
(n_vehicles, vehicle_list) = load_vehicle_from_text('VietVRP/data/vehicle.txt')
'''
print('Total capa: {}\nTotal demand: {}'.format(total_capacity(vehicle_list), total_demand(city_list)))
print('Scaler: {}'.format(total_capacity(vehicle_list)/ total_demand(city_list)))
'''
shuffle_index = [i for i in range(n_cities)]
shuffle_index = shuffle(shuffle_index)
city_list_shuffle = [city_list[i] for i in shuffle_index]
print(shuffle_index)

for city in city_list_shuffle: 
    city.print()