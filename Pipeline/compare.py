# Compare 2 thuật toán TSP có KMeans và không có KMeans

import json
import pandas as pd
def compare():
    with_kmeans = json.load(open('output/summary_TSP_with_Kmeans.json', 'r'))
    no_kmeans = json.load(open('output/summary_TSP_no_Kmeans.json', 'r'))

    data = [(str(with_kmeans['Distance']) + ' km', str(with_kmeans['Cost']), str(with_kmeans['Time']) + ' ms'),
            (str(float(no_kmeans['Distance'])) + ' km', str(no_kmeans['Cost']), str(no_kmeans['Time']) + ' ms')]

    df = pd.DataFrame(data, columns=['Distance','Cost', 'Time'], index=['TSP with Kmeans', 'TSP no Kmeans'])
    print('\n')
    print(df)
    print('\n')