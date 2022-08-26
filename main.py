import sys
import os
import matplotlib.pyplot as plt

from Pipeline.TSP_no_KMeans import TSP_no_Kmeans
from Pipeline.compare import compare
from Pipeline.plotting_data import plotting_for_phase1, plotting_for_pre_phase2
sys.path.append(os.getcwd())

from Pipeline.KMeans_phase import KMeans_phase
from Pipeline.TSP_phase import TSP_phase
from Pipeline.gendata import gendata
from Pipeline.pre_TSP_phase import Pre_TSP_phase
from graph_pygame import main

def dump_to(fname, mode, data):
    with open(fname, mode) as f:
    # with open('scenerios/no_kmeans/{}_vehicle.txt'.format(n_vehicle), 'w') as f:
        # f.write(details_tsp_no_kmeans)
        f.write(data)
        f.close()

details = []
summary = []
adding_to_detail = 'Scenerios: \n'
gendata_ret = ''
while gendata_ret not in ['y']:
    gendata_ret = input('1. Generate data? (Onlly \'y\' is approved ^^ ): ')

summary.append('1. Generate data: ')
details.append('1. Generate data: ')
details.append('\nDescription: randomly generate demand for each depot, customer and generate capacity for each vehicle\n')
if gendata_ret == 'y':
    while True:
        try:
            n_vehicle = input('\tNo. vehicle (type an int number in range (5-30) or \'s\' to skip, default = 15) = ')
            if n_vehicle == 's': 
                n_vehicle = 15
            else: 
                n_vehicle = int(n_vehicle)
            
            if n_vehicle>=5 and n_vehicle<=30: break
        except ValueError:
            print("Invalid input")

    summary.append('\tNo. vehicles = {}'.format(n_vehicle))
    
    details.append('\tNo. vehicles = {}'.format(n_vehicle))
    details.append('\tInput data list: ')
    details.append('\t\ttest_data/customers.csv')
    details.append('\t\ttest_data/depots.csv')
    details.append('\t\ttest_data/correlations.csv')
    details.append('\tOutput data to : ')
    details.append('\t\tinput/market.json')
    details.append('\t\tinput/depot.json')
    details.append('\t\tinput/correlation.json')
    details.append('\t\tinput/vehicle_{}.json\n\n'.format(n_vehicle))


    print('\tWaiting for generate data...')
    gendata(n_vehicle)
    print('Generate done!')
else: 
    while True:
        try:
            n_vehicle = int(input('Input a number to specify no. of vehicles scenarios: '))
            if os.path.exists(os.getcwd()+'\\input\\vehicle_{}.json'.format(n_vehicle)): break
            else: print('No data for {} vehicles, try again!'.format(n_vehicle))
        except ValueError:
            print("Invalid input")

    continue_flag = True
    while continue_flag:
        
        n_vehicle = int(n_vehicle)
        if os.path.exists(os.getcwd()+'\\input\\vehicle_{}.json'.format(n_vehicle)): continue_flag = False

    summary.append('\tNo gendata\n\n')
    details.append('\tNo gendata, use data in input/*')

adding_to_detail+='No. cluster = No. vehicle = {}\n'.format(n_vehicle)


print('2. Kmeans clustering phase:')

while True:
    show_text_flag = input('Do you want to show cluster\'s information? (y/n): ')
    if show_text_flag not in ['y', 'n']:
        print('Invalid input')
    else: break
if show_text_flag == 'y': show_text_flag = True
else: show_text_flag = False

summary_kmeans, details_kmeans, _ = KMeans_phase('input/vehicle_{}.json'.format(n_vehicle))
summary.append('2. KMeans clustering phase:')
summary.append(summary_kmeans)

details.append('2. KMeans clustering phase:')
details.append(details_kmeans)

plotting_for_phase1(show_text_flag)
plt.show()

print('3. Kmeans sub-clustering phase:')
print('Input some parameters: ')

while True:
    try:
        n_customers_threshold = input('\tNo. customers threshold (recommended a number in range (15, 30), type \'s\' to skip, default = 15): ')
        if n_customers_threshold == 's': n_customers_threshold = 15
        else: n_customers_threshold = int(n_customers_threshold)
        break
    except ValueError:
        print("Invalid input")

while True:
    show_text_flag = input('Do you want to show cluster\'s and sub-cluster\'s information? (y/n): ')
    if show_text_flag not in ['y', 'n']:
        print('Invalid input')
    else: break
if show_text_flag == 'y': show_text_flag = True
else: show_text_flag = False

summary_pre_tsp, details_pre_tsp = Pre_TSP_phase(n_customers_threshold, vehicle_fname='input/vehicle_{}.json'.format(n_vehicle))

adding_to_detail+='Maximal number of customers for TSP = {}\n\n'.format(n_customers_threshold)
summary.append('3. Kmeans sub-clustering phase:')
summary.append(summary_pre_tsp)

details.append('3. Kmeans sub-clustering phase:')
details.append(details_pre_tsp)

dump_summary_fname = 'scenerios/summary/{}_vehicle_{}_node_threshold.txt'.format(n_vehicle, n_customers_threshold)
dump_details_fname = 'scenerios/details/{}_vehicle_{}_node_threshold.txt'.format(n_vehicle, n_customers_threshold)

dump_to(dump_summary_fname, 'w', '\n'.join(summary)+ '\n\nMore details in {}'.format(dump_details_fname))
dump_to(dump_details_fname, 'w', adding_to_detail + '\n'.join(details))

plotting_for_pre_phase2(show_text_flag)
plt.show()

print('4. TSP phase:')
summary_tsp, details_tsp, _, _, _ = TSP_phase(n_vehicle)

summary.append('4. TSP phase:')
summary.append(summary_tsp)

details.append('4. TSP phase:')
details.append(details_tsp)

print('5. TSP no kmeans:')
_,_,_, details_tsp_no_kmeans = TSP_no_Kmeans(n_vehicle)

compare()
# Dump ra file txt

dump_to(dump_summary_fname, 'w', '\n'.join(summary)+ '\n\nMore details in {}'.format(dump_details_fname))
dump_to(dump_details_fname, 'w', adding_to_detail + '\n'.join(details))
dump_to('scenerios/no_kmeans/{}_vehicle.txt'.format(n_vehicle), 'w', details_tsp_no_kmeans)

print('6. Plotting TSP phase by pygame: ')
main()
