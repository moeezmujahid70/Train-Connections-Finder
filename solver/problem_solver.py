# Parses problems.csv and solves them
import pandas as pd
import csv
import heapq
import networkx as nx
from itertools import groupby

def load_problems_csv(problems_file_path: str) -> pd.DataFrame:
    """
    Loads and preprocesses the problems CSV file.
    """
    try:
        # Load the CSV
        problems_df = pd.read_csv(problems_file_path)

        # Split 'CostFunction' into two columns if applicable
        if 'CostFunction' in problems_df.columns:
            problems_df[['CostFunction', 'time']] = problems_df['CostFunction'].str.split(
                ' ', expand=True, n=1)

        return problems_df

    except FileNotFoundError:
        print(f"Error: File not found at {problems_file_path}")
        raise
    except pd.errors.ParserError:
        print("Error: Failed to parse the CSV file. Please check its format.")
        raise


def read_and_preprocess_csv(schedule_file_path: str) -> pd.DataFrame:
    """
    Loads and preprocesses the schedule dataset.
    """
    # Load the CSV
    df = pd.read_csv(schedule_file_path)

    # Drop unnecessary columns
    columns_to_drop = [
        'Station Name',
        'source Station Name',
        'Destination station Code',
        'Destination Station Name'
    ]
    schedule_df = df.drop(columns=columns_to_drop, errors='ignore')

    # Strip unwanted characters from relevant columns
    schedule_df['Train No.'] = schedule_df['Train No.'].str.strip("'")
    schedule_df['Arrival time'] = schedule_df['Arrival time'].str.strip("'")
    schedule_df['Departure time'] = schedule_df['Departure time'].str.strip(
        "'")
    schedule_df['station Code'] = schedule_df['station Code'].str.strip()

    return schedule_df

def dijkstra_path(graph, start, stop):
    # Initialize distances to infinity and set the start node distance to 0
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    # Dictionary to store the predecessor of each node to reconstruct the path
    predecessors = {node: {'previous_station': None, 'train': None} for node in graph}
    
    # Priority queue to keep track of nodes to visit
    priority_queue = [(0, start)]  # (distance, node)
    
    while priority_queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If we reach the target node, stop and reconstruct the path
        if current_node == stop:
            station_sequence = []
            train_sequence = []
            while current_node is not None:
                station_sequence.append(current_node)
                if predecessors[current_node]['train'] is not None:
                    train_sequence.append(predecessors[current_node]['train'])
                current_node = predecessors[current_node]['previous_station']
            return station_sequence[::-1], train_sequence[::-1], distances[stop]  # Reverse path to get it from start to target
        
        # If the distance in queue is greater than the known distance, skip it
        if current_distance > distances[current_node]:
            continue
        
        # Check neighbors of the current node
        for neighbor, attribute in graph[current_node].items():
            distance = current_distance + attribute['weight']
            
            # Only update if the new distance is shorter
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = {'previous_station': current_node, 'train': attribute['train']}  # Set predecessor
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # If target is unreachable, return an empty path and distance infinity
    return None, None, None


def solve_cost_stop(graph, start, stop, schedule_df):
    station_sequence, train_sequence, distance = dijkstra_path(graph, start, stop)
    
    if station_sequence is None:
        return 'PATH NOT FOUND'
    
    identical_train_groups = [list(y) for _, y in groupby(train_sequence)]
    
    station_seq = [station_sequence[0]]
    counter = 0
    for identical_train_group in identical_train_groups:
        #print(z_dash)
        counter += len(identical_train_group)
        station_seq.append(station_sequence[counter])
    train_seq = []
    for identical_train_group in identical_train_groups:
        train_seq += list(set(identical_train_group))
    #print(train_seq)
    #print(station_seq)
    station_isl_seq = []
    for i in range(len(train_seq)):
        first_station_found = False
        second_station_found = False
        train_no = train_seq[i]
        rslt_df = schedule_df.loc[schedule_df['Train No.'] == train_no]
        for _, row in rslt_df.iterrows():
            if row['station Code'] == station_seq[i] and not first_station_found:
                station_isl_seq.append(row['islno'])
                first_station_found = True
            if row['station Code'] == station_seq[i+1] and not second_station_found:
                station_isl_seq.append(row['islno'])
                second_station_found = True
            if first_station_found and second_station_found:
                break
            
    solution = []
    station_isl_seq = [station_isl_seq[pos:pos + 2] for pos in range(0, len(station_isl_seq), 2)]
    #print(station_isl_seq)
    
    for i in range(len(train_seq)):
        solution.append(str(train_seq[i]))
        solution.append(' : ')
        solution.append(str(station_isl_seq[i][0]))
        solution.append(' -> ')
        solution.append(str(station_isl_seq[i][1]))
        solution.append(' ; ')
    solution = solution[:-1]+[','+str(distance)]
    return ''.join(solution)



def create_solutions_csv(solutions: dict, filename: str):
    """
    Generates a solutions CSV file.
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Writing the header
            writer.writerow(['ProblemNo', 'Connection', 'Cost'])

            # Writing the data
            for problem_no, info in solutions.items():
                writer.writerow([problem_no, info.get(
                    'Connection', ''), info.get('Cost', '')])
        print(f"Solutions successfully written to {filename}")

    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
