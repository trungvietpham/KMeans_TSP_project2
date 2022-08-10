# Compare 2 thuật toán TSP có KMeans và không có KMeans

import json
import pandas as pd
with_kmeans = json.load(open('output/summary_TSP_with_Kmeans.json', 'r'))
no_kmeans = json.load(open('output/summary_TSP_no_Kmeans.json', 'r'))

data = [(str(with_kmeans['Distance']) + ' km', with_kmeans['Time']),
        (no_kmeans['Distance'], no_kmeans['Time'])]

df = pd.DataFrame(data, columns=['Distance', 'Time'], index=['TSP with Kmeans', 'TSP no Kmeans'])
print(df)