import sys
import os
sys.path.append(os.getcwd())
from utils.get_data import *

#csv_to_txt('test_data/test_data_30.csv', 'input/tmp.txt')
def gendata(n_vehicle = 15):
    csv_to_json_file('test_data/customers.csv', data_type='market', mode='w', high_threshold=500)
    gen_vehicle(n_vehicle, n_items=2, dump_file='input/vehicle_{}.json'.format(n_vehicle), low_threshold=3000, high_threshold=10000, n_types=3)
    csv_to_json_file('test_data/depots.csv', data_type='depot', mode='w', low_threshold=1000, high_threshold=5000)

    get_length_path('test_data/correlations.csv', 'input/correlation.json')

if __name__ == '__main__':
    gendata()