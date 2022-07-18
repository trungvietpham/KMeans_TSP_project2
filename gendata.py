from utils.get_data import *

#csv_to_txt('test_data/test_data_30.csv', 'input/tmp.txt')
csv_to_json_file('test_data/customers.csv', data_type='market', mode='w')
gen_vehicle(25, n_items=2, dump_file='input/vehicle.json')
csv_to_json_file('test_data/depots.csv', data_type='depot', mode='w', low_threshold=0, high_threshold=10000)

get_length_path('test_data/correlations.csv', 'input/correlation.json')