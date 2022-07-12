from sklearn.utils import shuffle
import json

import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils.utils import load_node_from_text, load_vehicle_from_text, total_capacity, total_demand

f = open('output/phase2.json', 'r')
data = json.load(f)

