from pprint import pprint
import math
import glob
import copy
import matplotlib.pyplot as plt
import numpy as np
from graph import *

# Returns a dict with all trolleybuses time_table for each station
def read_all_data(path):
    stations_dict = {}
    for file_name in glob.glob(path):
        station_name = find_between(file_name, '/', '.')
        if station_name != 'station_graph':
            stations_dict[station_name] = read_data(file_name)
    # pprint(data_obj)
    return stations_dict

# Gives the name of the station based on location of the file
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Gives a data dict composed of troleybuses and its specific times only in minutes
def read_data(file_name):
    lines = open(file_name).read().splitlines()
    lines = {int(line.split(') ')[0]):line.split(') ')[1].split(', ') for line in lines}
    trolleybus_minutes_dict = {}
    for trolleybus in lines:
        minutes =  [int(time.split(':')[0]) * 60 + int(time.split(':')[1])
            for time in lines[trolleybus]]
        trolleybus_minutes_dict[trolleybus] = minutes

    trolleybus_minutes_dict =  {trolleybus :
        [int(time.split(':')[0]) * 60 + int(time.split(':')[1]) for time in lines[trolleybus]]
        for trolleybus in lines}
    # pprint(dict_trolleybus_minutes)
    return trolleybus_minutes_dict

# Calls the generate_coordinates and generate_plot functions
def visualise_data(data_obj,data_obj_new):
    trolleybus_xy_values_dict = {}
    trolleybus_xy_values_dict_new = {}
    y_change = 0.25
    trolleybus_xy_values_dict = generate_coordinates(data_obj,0)
    trolleybus_xy_values_dict_new = generate_coordinates(data_obj_new,y_change)
    # pprint(trolleybus_xy_values_dict)
    generate_plot(y_change, data_obj.keys(), trolleybus_xy_values_dict, trolleybus_xy_values_dict_new)
    # rgb_colors = get_spaced_colors(len)
    # pprint(y_ticks)
    # pprint(y_labels)

# Generate trolleybus:[x_list,y_list] coordinates dict based on data_obj
def generate_coordinates(data_obj,y_change):
    trolleybus_xy_values_dict = {}
    for i, station_name in enumerate(sorted(data_obj.keys())):
        for trolleybus,time_tabel in data_obj[station_name].items():
            if trolleybus not in trolleybus_xy_values_dict.keys():
                trolleybus_xy_values_dict[trolleybus] = {'x':[], 'y':[]}
                for minute in time_tabel:
                    trolleybus_xy_values_dict[trolleybus]['x'].append(minute)
                    trolleybus_xy_values_dict[trolleybus]['y'].append(i + y_change)
            else:
                for minute in time_tabel:
                    trolleybus_xy_values_dict[trolleybus]['x'].append(minute)
                    trolleybus_xy_values_dict[trolleybus]['y'].append(i + y_change)
    return trolleybus_xy_values_dict

# Generate a plot based the coordinates given
def generate_plot(y_change, station_name, trolleybus_xy_values_dict, trolleybus_xy_values_dict_new):
    y_ticks = []
    y_labels = []
    for i, station_name in enumerate(sorted(station_name)):
        y_ticks.append(i)
        y_labels.append(station_name)
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_subplot(111)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    colors = gen_colors(len(trolleybus_xy_values_dict.keys()))
    for i, trolleybus in enumerate(trolleybus_xy_values_dict.keys()):
        ax.plot(trolleybus_xy_values_dict[trolleybus]['x'],
            trolleybus_xy_values_dict[trolleybus]['y'], 'o',
            color=colors[i], alpha=0.25)
        ax.plot(trolleybus_xy_values_dict_new[trolleybus]['x'],
            trolleybus_xy_values_dict_new[trolleybus]['y'], 'o',
            color=colors[i], label=trolleybus)
    ax.legend(loc='upper right', ncol=1, bbox_to_anchor=(1.1,1))
    plt.show()

# Generate n differant colors
def gen_colors(n):
    cmap = plt.get_cmap('gist_rainbow')
    colors = cmap(np.linspace(0,1,n))
    return colors

 # Obtains a new data_obj based on the implemented algorithm and prints the coef
def optimize_data(data_obj):
    data_obj_new = copy.deepcopy(data_obj)
    station_gaps_dict = find_gaps(data_obj)
    coef = compute_coef(station_gaps_dict)
    print("Initial coef: {}".format(coef))
    trolleybus_shift_dict = {trol:0 for trol in sorted(set([trolleybus for station_timetable in data_obj.values()
        for trolleybus in station_timetable]))}
    for trolleybus in sorted(list(set([trolleybus for station_timetable in data_obj.values()
        for trolleybus in station_timetable])))[1:]:
        coef1 = coef2 = coef
        data_obj_new1 = copy.deepcopy(data_obj_new)
        data_obj_new2 = copy.deepcopy(data_obj_new)
        shifts1 = shifts2 = 0
        while(1):
            data_obj_temp = shift_route(trolleybus,data_obj_new1,1)
            station_gaps_dict = find_gaps(data_obj_temp)
            coef_temp = compute_coef(station_gaps_dict)
            if coef_temp < coef1:
                shifts1 += 1
                data_obj_new1 = data_obj_temp
                coef1 = coef_temp
            else:
                break
        while(1):
            data_obj_temp = shift_route(trolleybus,data_obj_new2,-1)
            station_gaps_dict = find_gaps(data_obj_temp)
            coef_temp = compute_coef(station_gaps_dict)
            if coef_temp < coef2:
                shifts2 += -1
                data_obj_new2 = data_obj_temp
                coef2 = coef_temp
            else:
                break

        if coef1 < coef2:
            coef = coef1
            data_obj_new = data_obj_new1
            trolleybus_shift_dict[trolleybus] = shifts1
        else:
            coef = coef2
            data_obj_new = data_obj_new2
            trolleybus_shift_dict[trolleybus] = shifts2

    print("Optimized coef: {}".format(coef))
    output_shifts(trolleybus_shift_dict)

    return data_obj_new

# Find all gaps between trolleybuses, return a station_name:gaps_list dict
def find_gaps(data_obj):
    station_arrival_dict = {station:
        sorted([minute for trolleybus_timetabel in station_timetables.values()
        for minute in trolleybus_timetabel])
        for station,station_timetables in data_obj.items()}
    station_gaps_dict = {station:
        [arrival_list[i+1]-arrival_list[i] for i in range(len(arrival_list)-1)]
        for station, arrival_list in station_arrival_dict.items()}
    return station_gaps_dict

# Compute needed coeficient
def compute_coef(station_gaps_dict):
    sum_exp = 0
    for gaps_list in station_gaps_dict.values():
        for gap in gaps_list:
            sum_exp += math.exp(gap)
    return sum_exp

# Shift specified trolleybus's timetable 1 minute right or left
def shift_route(trolleybus, data_obj, direction_value):
    data_obj_new = copy.deepcopy(data_obj)
    for station_name, station_timetabel in data_obj_new.items():
        for trol_num, arrival_list in station_timetabel.items():
            if trol_num == trolleybus:
                for i in range(len(data_obj_new[station_name][trol_num])):
                    data_obj_new[station_name][trol_num][i] += direction_value
    return data_obj_new

# Output optimize shift
def output_shifts(trolleybus_shift_dict):
    for trolleybus,shift in trolleybus_shift_dict.items():
        print("{} troleybuses: {} minute shift".format(trolleybus,shift))

#find the min nr of trolleybuses for each route needed
def find_nr_trolleybuses(station_graph):
    trolleybus_num_dict = {}
    working_station_graph = copy.deepcopy(station_graph)
    max_routes = find_max_routes_station(station_graph)
    for num in range(1,max_routes+1):
        station_routes_dict = find_needed_stations(num, station_graph)
        for check_station,routes_list in station_routes_dict.items():
            mini_trolleybus_num_dict = find_needed_trolleybus(check_station, routes_list, working_station_graph)
            # pprint(mini_trolleybus_num_dict)
            #add determined nr of trolleybusses to trolleybus_num_dict
            for trolleybus, nr_trolleybuses in mini_trolleybus_num_dict.items():
                if trolleybus not in trolleybus_num_dict.keys():
                    trolleybus_num_dict[trolleybus] = nr_trolleybuses
                else:
                    trolleybus_num_dict[trolleybus] += nr_trolleybuses
            # pprint(trolleybus_num_dict)
            subtract_passangers(mini_trolleybus_num_dict, working_station_graph)
    #graph print to see amount of people remained for each conn
    print("Graph after with people after the trolleybuses take all people:\n")
    pprint(working_station_graph)
    return trolleybus_num_dict

# return dict of station: routes_list for specied number of routes
def find_needed_stations(nr_routes_per_station,station_graph):
    return {station:station_graph[station]['trolleybus_list']
        for station in station_graph.keys()
        if len(station_graph[station]['trolleybus_list']) == nr_routes_per_station}

# finds max nr of routes that a station can have
def find_max_routes_station(station_graph):
    return max(set([len(station_graph[station]['trolleybus_list'])
        for station in station_graph.keys()]))

# returns dict with nr of trolleybuses for each route of this check_station
def find_needed_trolleybus(check_station, routes_list, working_station_graph):
    max_persons_in_trolleybus = 70
    nr_people = find_nr_people(check_station, working_station_graph)
    # print(nr_people)
    nr_trolleybuses = nr_people/max_persons_in_trolleybus
    trolleybus_num_dict = {route:(math.ceil(nr_trolleybuses/len(routes_list))
        if i==0 else math.floor(nr_trolleybuses/len(routes_list)) )
        for i, route in enumerate(routes_list)}
    return trolleybus_num_dict

# find nr of people for station that we are checking
def find_nr_people(check_station, working_station_graph):
    for station_name in working_station_graph.keys():
        for conn, nr_people in working_station_graph[station_name]['conn'].items():
            if conn == check_station:
                return nr_people
    # if did't return from previous loop then check_station is a starting station
    # will work only if starting station has one path
    for station_name in working_station_graph.keys():
        if station_name == check_station:
            for conn, nr_people in working_station_graph[station_name]['conn'].items():
                return nr_people

def subtract_passangers(mini_trolleybus_num_dict, working_station_graph):
    for trolleybus, nr_trolleybuses in mini_trolleybus_num_dict.items():
        for station in working_station_graph.keys():
            for conn in working_station_graph[station]['conn'].keys():
                if trolleybus in working_station_graph[conn]['trolleybus_list']:
                    working_station_graph[station]['conn'][conn] -= nr_trolleybuses*70
                    if working_station_graph[station]['conn'][conn] < 0:
                        working_station_graph[station]['conn'][conn] = 0

def main():
    path = "stations/*.txt"
    data_obj = read_all_data(path) #obtain data object
    data_obj_reduced = {station:station_timetabel
        for station,station_timetabel in copy.deepcopy(data_obj).items()
        if station=='stefan_cel_mare'}
    print("Subproblem 1")
    data_obj_prob1 = optimize_data(data_obj_reduced)
    visualise_data(data_obj_reduced,data_obj_prob1)
    print("\nSubproblem 2")
    data_obj_prob2 = optimize_data(data_obj)
    visualise_data(data_obj,data_obj_prob2)
    print("\nSubproblem3")
    trolleybus_num_dict = find_nr_trolleybuses(get_station_graph())
    for trolleybus, nr_trolleybuses in trolleybus_num_dict.items():
        print("Route {}: {} trolleybus needed".format(trolleybus, nr_trolleybuses))
main()
