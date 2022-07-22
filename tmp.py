from lib2to3.pytree import convert
from utils.utils import *

# print(get_mean_latlong_to_meter())
cluster_data = json.load(open('output/phase2_market.json', 'r'))

print(cluster_data['0'])