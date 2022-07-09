from sklearn.utils import shuffle

import sys
sys.path.append("D:/TaiLieuHocTap/Năm 3- Kỳ 2/Project 2/Source code/VietVRP")
from utils import load_node_from_text, load_vehicle_from_text, total_capacity, total_demand


a = {}
a[1] = 2
a[3] = 5
a[1] += 4
keys = a.keys
for key in a:
    print('Key: {}, value: {}'.format(key, a[key]))
