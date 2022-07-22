import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils.get_data import *

#csv_to_txt('test_data/test_data_30.csv', 'input/tmp.txt')
csv_to_json_file('test_data/customers.csv', data_type='market', mode='w', high_threshold=500)
gen_vehicle(15, n_items=2, dump_file='input/vehicle.json', low_threshold=3000, high_threshold=10000)
csv_to_json_file('test_data/depots.csv', data_type='depot', mode='w', low_threshold=1000, high_threshold=5000)

get_length_path('test_data/correlations.csv', 'input/correlation.json')