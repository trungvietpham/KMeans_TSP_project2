import sys
import os
sys.path.append(os.getcwd())
from utils.get_data import *

#csv_to_txt('test_data/test_data_30.csv', 'input/tmp.txt')
def gendata(n_vehicle = 15):
    #Đọc các thông tin cấu hình từ file config.txt
    with open(r'config/config.txt', 'r') as f:
        config = f.read()
    config = config.split('\n')
    n_types = int(config[0].split('=')[1].strip())

    coef_list = config[1].split('=')[1].replace(' ', '')
    if len(coef_list) < 3: coef_list = None
    else: 
        coef_list = coef_list[1:-1].split(',')
        coef_list = list(map(float, coef_list))

    n_items = 2
    if config[2].find('n_items')>=0: 
        n_items = int(config[2].split('=')[1].strip())
        save_items_f = open('input/item.txt', 'w')
        save_items_f.write(str(n_items))

    csv_to_json_file('test_data/customers.csv', data_type='market', mode='w', high_threshold=500, n_items=n_items)
    gen_vehicle(n_vehicle, n_items=n_items, dump_file='input/vehicle_{}.json'.format(n_vehicle), low_threshold=3000, high_threshold=10000, n_types=n_types, coef_list=coef_list)
    csv_to_json_file('test_data/depots.csv', data_type='depot', mode='w', low_threshold=1000, high_threshold=5000, n_items=n_items)

    get_length_path('test_data/correlations.csv', 'input/correlation.json')

if __name__ == '__main__':
    gendata()