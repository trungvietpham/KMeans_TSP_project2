
from ast import dump
from dbm import dumb
import random
import numpy as np
import pandas as pd
import json
import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")

def csv_to_json_file(csv_file, n_items = 2, data_type = 'market', low_threshold = 0, high_threshold = 1000, mode = 'w'):
    '''
    JSON:
    'market': {
        number: {
            'id': 
            'name': 
            'location': {
                'lat': x
                'long': y
            }
            'demand_list':{
                number: {
                    'id': id
                    'demand': demand
                }
            }
        }
    }
    '''
    df = pd.read_csv(csv_file)
    # print(df)
    save_data = {}
    # save_data['length'] = len(df)
    markets_dict = {}

    

    cnt = 0
    
    for line in range(len(df)):
        market_dict = {}
        market_dict['id'] = cnt
        market_dict['code'] = df['code'][line][0]+str(cnt)
        market_dict['name'] = df['name'][line]
        location_dict = {}
        # if float(df['latitude'][line]) < 18: continue
        location_dict['lat'] = float(df['latitude'][line])
        location_dict['long'] = float(df['longitude'][line])
        market_dict['location'] = location_dict
        demands_dict = {}

        for item in range(n_items):
            gen_num = random.randint(low_threshold, high_threshold)
            if gen_num!=0:
                demand_dict = {'item_id':item+1, 'demand': gen_num}
                demands_dict[item+1] = demand_dict
        market_dict['demand_list'] = demands_dict

        markets_dict[cnt] = market_dict
        cnt+=1
        
    
    save_data[data_type] = markets_dict
    with open('input/'+data_type+'.json', mode, encoding='utf8') as json_file:
        json.dump(save_data, json_file, ensure_ascii=False, indent=4)

def gen_vehicle(n_vehicle, n_items, dump_file, low_threshold = 0, high_threshold = 10000, n_types = 3):
    save_data = {}
    coef_list = []
    for _ in range(n_types):
        coef_list.append(round(random.randint(30, 300)/30, 1))
    

    for i in range(n_vehicle):
        vehicle_i = {}
        v_type = random.randint(1, 3)
        vehicle_i['type'] = v_type
        vehicle_i['coef'] = coef_list[v_type-1]
        for j in range(n_items):
            gen_num = random.randint(low_threshold, high_threshold)
            if gen_num!=0:
                demand_dict = {'item_id':j+1, 'demand': gen_num}
                vehicle_i[j+1] = demand_dict
        save_data[i] = vehicle_i
    
    json.dump(save_data, open(dump_file, 'w'), indent=4)

def mapping_id_code(csv_file):
    df = pd.read_csv(csv_file)
    # print(df)
    save_data = {}
    # save_data['length'] = len(df)

    for line in range(len(df)):
        # if float(df['latitude'][line]) < 18: continue
        save_data[df['code'][line]] = line
    return save_data


def get_length_path(csv_file, dump_file):
    
    df = pd.read_csv(csv_file)
    # print(df)
    customer_map = mapping_id_code('test_data/customers.csv')
    depot_map = mapping_id_code('test_data/depots.csv')
    # print(customer_map)
    node_map = {**customer_map, **depot_map}
    # print(node_map)
    save_data = {}
    for line in range(len(df)):
        from_node_code = str(df['from_node_code'][line])
        to_node_code = str(df['to_node_code'][line])
        distance = float(df['distance'][line])
        # print('from: {}, to: {}'.format(from_node_code, to_node_code))
        # print(node_map[to_node_code])
        head = from_node_code[0] + str(node_map[from_node_code])
        tail = to_node_code[0] + str(node_map[to_node_code])
        if head not in save_data: 
            save_data[head] = {}
        save_data[head][tail] = distance
    
    json.dump(save_data, open(dump_file, 'w'), indent=4)

