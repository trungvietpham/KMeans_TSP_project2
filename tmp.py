from lib2to3.pytree import convert
from utils.utils import *

# print(get_mean_latlong_to_meter())
convert_coef = get_convert_coef_from_file('input/latlong_to_meter_coef.txt')
print(convert_coef)