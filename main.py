from Pipeline.KMeans_phase import KMeans_phase
from Pipeline.TSP_phase import TSP_phase
from Pipeline.gendata import gendata
from Pipeline.pre_TSP_phase import Pre_TSP_phase
from graph_pygame import main


gendata_ret = input('1. Generate data? (y/n): ')
if gendata_ret == 'y':
    n_vehicle = input('\tNo. vehicle (type an int number or \'s\' to skip, default = 15) = ')
    if n_vehicle == 's': n_vehicle = 15
    else: n_vehicle = int(n_vehicle)
    print('\tWaiting for generate data...')
    gendata(n_vehicle)
    print('Generate done!')

print('2. Kmeans clustering phase:')
KMeans_phase()

print('3. Clustering each cluster into smaller clusters before step over TSP phase:')
print('Input some parameters: ')
n_node_threshold = input('\tNo. node threshold (recommended a number in range (15, 30), type \'s\' to skip, default = 15): ')
if n_node_threshold == 's': n_node_threshold = 15
else: n_node_threshold = int(n_node_threshold)
Pre_TSP_phase(n_node_threshold)

print('4. TSP phase:')
TSP_phase()

print('5. Plotting TSP phase by pygame: ')
main()
