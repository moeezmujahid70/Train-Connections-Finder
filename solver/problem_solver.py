# Parses problems.csv and solves them
import pandas as pd
import heapq
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

# -------------------------COst Funtion Stop ---------------------------------


def dijkstra_path(graph, start, target):
    # Initialize costs to infinity and set the start node cost to 0
    costs = {node: float('infinity') for node in graph}
    costs[start] = 0

    # Dictionary to store the predecessor of each node to reconstruct the path
    predecessors = {node: {'previous_station': None, 'train': None}
                    for node in graph}

    # Priority queue to keep track of nodes to visit
    priority_queue = [(0, start)]  # (cost, node)

    while priority_queue:
        # Get the node with the smallest cost
        current_cost, current_node = heapq.heappop(priority_queue)

        # If we reach the target node, stop and reconstruct the path
        if current_node == target:
            station_sequence = []
            train_sequence = []
            while current_node is not None:
                station_sequence.append(current_node)
                if predecessors[current_node]['train'] is not None:
                    train_sequence.append(predecessors[current_node]['train'])
                current_node = predecessors[current_node]['previous_station']
            # Reverse path to get it from start to target
            return station_sequence[::-1], train_sequence[::-1], costs[target]

        # If the cost in queue is greater than the known cost, skip it
        if current_cost > costs[current_node]:
            continue

        # Check neighbors of the current node
        for neighbor, attribute in graph[current_node].items():
            cost = current_cost + attribute['weight']

            # Only update if the new cost is shorter
            if cost < costs[neighbor]:
                costs[neighbor] = cost
                predecessors[neighbor] = {
                    'previous_station': current_node, 'train': attribute['train']}  # Set predecessor
                heapq.heappush(priority_queue, (cost, neighbor))

    # If target is unreachable, return an empty path and cost infinity
    return None, None, None


def solve_cost_stop(graph, start, target, schedule_df):
    station_sequence, train_sequence, cost = dijkstra_path(
        graph, start, target)

    if station_sequence is None:
        return 'PATH NOT FOUND'

    identical_train_groups = [list(y) for _, y in groupby(train_sequence)]

    station_seq = [station_sequence[0]]
    counter = 0
    for identical_train_group in identical_train_groups:
        counter += len(identical_train_group)
        station_seq.append(station_sequence[counter])
    train_seq = []
    for identical_train_group in identical_train_groups:
        train_seq += list(set(identical_train_group))
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

    connection = []
    station_isl_seq = [station_isl_seq[pos:pos + 2]
                       for pos in range(0, len(station_isl_seq), 2)]

    for i in range(len(train_seq)):
        connection.append(str(train_seq[i]))
        connection.append(' : ')
        connection.append(str(station_isl_seq[i][0]))
        connection.append(' -> ')
        connection.append(str(station_isl_seq[i][1]))
        connection.append(' ; ')
    connection = connection[:-1]  # +[','+str(cost)]
    return ''.join(connection), str(cost)


#   ----------------- Cost Funtion TimeIntrain --------------------------


def dijkstra_path_timeintrain(graph, start, target):
    # Initialize costs to infinity and set the start node cost to 0
    costs = {node: float('infinity') for node in graph}
    costs[start] = 0

    # Dictionary to store the predecessor of each node to reconstruct the path
    predecessors = {node: {'previous_station': None, 'train': None}
                    for node in graph}

    # Priority queue to keep track of nodes to visit
    priority_queue = [(0, start)]  # (current_cost, current_node)

    while priority_queue:
        # Get the node with the smallest cost
        current_cost, current_node = heapq.heappop(priority_queue)

        # If we reach the target node, stop and reconstruct the path
        if current_node == target:
            # Reconstruct the optimal path
            station_sequence = []
            train_sequence = []
            while current_node is not None:
                station_sequence.append(current_node)
                if predecessors[current_node]['train'] is not None:
                    train_sequence.append(predecessors[current_node]['train'])
                current_node = predecessors[current_node]['previous_station']
            return station_sequence[::-1], train_sequence[::-1], costs[target]

        # Skip if cost is already outdated
        if current_cost > costs[current_node]:
            continue

        # Check neighbors for the next possible steps
        for neighbor, attribute in graph[current_node].items():
            travel_cost = current_cost + attribute['timeintrain']

            # Only update if this path is shorter
            if travel_cost < costs[neighbor]:
                costs[neighbor] = travel_cost
                predecessors[neighbor] = {
                    'previous_station': current_node,
                    'train': attribute['train']
                }
                heapq.heappush(priority_queue, (travel_cost, neighbor))

    # Return if target unreachable
    return None, None, None


def solve_cost_timeintrain(graph, start, target, schedule_df):
    station_sequence, train_sequence, total_cost = dijkstra_path_timeintrain(
        graph, start, target)

    if station_sequence is None:
        return 'PATH NOT FOUND'

    from itertools import groupby

    # Group by identical trains
    identical_train_groups = [list(y) for _, y in groupby(train_sequence)]

    station_seq = [station_sequence[0]]
    counter = 0
    for identical_train_group in identical_train_groups:
        counter += len(identical_train_group)
        station_seq.append(station_sequence[counter])

    train_seq = []
    for identical_train_group in identical_train_groups:
        train_seq += list(set(identical_train_group))

    # Construct connections in the expected format
    connection = []
    for i in range(len(train_seq)):
        # Get islno for both stations
        train_no = train_seq[i].strip()
        start_station = station_seq[i]
        end_station = station_seq[i + 1]

        # Fetch the islno from schedule_df
        start_islno = schedule_df[(schedule_df['Train No.'] == train_no) &
                                  (schedule_df['station Code'] == start_station)]['islno'].values[0]
        end_islno = schedule_df[(schedule_df['Train No.'] == train_no) &
                                (schedule_df['station Code'] == end_station)]['islno'].values[0]

        # Append formatted solution
        connection.append(f"{train_no} : {start_islno} -> {end_islno}")

    return ' ; '.join(connection), str(total_cost)


def create_solutions_csv(solutions: dict, filepath: str):
    """
    Generates a solutions CSV file.
    """
    try:
        solutions_df = pd.DataFrame(solutions)
        solutions_df.to_csv(filepath, index=False)
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
