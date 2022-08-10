from ast import dump
import codecs
from distutils.command.config import dump_file
from math import dist
from time import time
import numpy as np
import json
from python_tsp.exact import solve_tsp_dynamic_programming

import sys
import os

from utils.utils import get_convert_coef_from_file, load_item_from_text, load_node_from_json, load_vehicle_from_json
sys.path.append(os.getcwd())

def get_nearest_depot(point, depot_list):
    pass

def get_nearest_node(start_node, length_matrix):
    pass

def main(n_vehicle):
    # Load các thông tin về vehicle, depot, correlation
    correlation = json.load(open('input/correlation.json', 'r'))
    depot_data = json.load(codecs.open('input/depot.json', 'r', 'utf-8-sig'))

    (n_items, item_list) = load_item_from_text('input/item.txt')
    #(n_cities, city_list) = load_node_from_text(city_fname, format='market', n_items=n_items)
    (n_cities, city_list) = load_node_from_json('input/market.json', format='market', n_items=n_items)
    (n_vehicles, vehicle_list) = load_vehicle_from_json('input/vehicle_{}.json'.format(n_vehicle), n_items=n_items)
    convert_coef = get_convert_coef_from_file('input/latlong_to_meter_coef.txt')

    ignore_list = []
    