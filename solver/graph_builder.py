from datetime import datetime, timedelta
import pandas as pd
import networkx as nx


# Note: might need to implement threading for later CostFuntions Graphs

def calculate_travel_time(from_station, to_station) -> timedelta:

    # Parse departure and arrival times
    departure_time = datetime.strptime(
        from_station['Departure time'].strip("'"), "%H:%M:%S")
    arrival_time = datetime.strptime(
        to_station['Arrival time'].strip("'"), "%H:%M:%S")

    # Handle overnight travel where arrival time is on the next day
    if arrival_time < departure_time:
        arrival_time += timedelta(days=1)

    return (arrival_time - departure_time)

def calculate_time(from_time, to_time):
    from_time = datetime.strptime(
        from_time.strip("'"), "%H:%M:%S")
    to_time = datetime.strptime(
        to_time.strip("'"), "%H:%M:%S")

    # Handle overnight travel where arrival time is on the next day
    if to_time < from_time:
        to_time += timedelta(days=1)
        
    return (to_time - from_time)


def build_graph(schedule_df: pd.DataFrame) -> nx.MultiDiGraph:
    """
    Builds a directed multigraph from the schedule data using NetworkX, allowing multiple edges between nodes.
    """
    G = nx.MultiDiGraph()  # MultiDiGraph allows multiple edges between nodes

    # Group by train number to handle consecutive stops for each train
    for train_no, group in schedule_df.groupby('Train No.'):
        group = group.sort_values('islno')  # Sort by stop order (islno)

        # Iterate through consecutive stops for each train
        for i in range(len(group) - 1):
            from_station = group.iloc[i]['station Code']
            to_station = group.iloc[i + 1]['station Code']
            departure_time = group.iloc[i]['Departure time']
            arrival_time = group.iloc[i + 1]['Arrival time']
            from_islno = group.iloc[i]['islno']
            to_islno = group.iloc[i+1]['islno']
            # Calculate travel time in seconds
            travel_time_seconds = calculate_travel_time(
                group.iloc[i], group.iloc[i + 1]).seconds

            # Add a directed edge with train-specific attributes
            G.add_edge(
                from_station,
                to_station,
                train=train_no,  # Each edge has a specific train number
                stops=1,  # Default weight (for Stops cost function)
                timeintrain=travel_time_seconds,  # Travel time in seconds
                departuretime=departure_time,
                arrivaltime=arrival_time,
                fromislno=from_islno,
                toislno=to_islno
            )

    return G

def expand_graph(graph: nx.MultiDiGraph) -> nx.DiGraph:
    
    arr_node_dict = {node: {} for node in graph}
    dep_node_dict = {node: {} for node in graph}
    expanded_graph = nx.DiGraph()
    
    for node in graph:
        for in_edge in graph.in_edges(node, data=True):
            expanded_graph.add_edge((in_edge[0], in_edge[2]['train'], in_edge[2]['fromislno'], 'dep'), (node,  in_edge[2]['train'], in_edge[2]['toislno'], 'arr'), time=in_edge[2]['timeintrain'])
            arr_node_dict[node][(node,  in_edge[2]['train'], in_edge[2]['toislno'], 'arr')] = in_edge[2]['arrivaltime']
            dep_node_dict[in_edge[0]][(in_edge[0], in_edge[2]['train'], in_edge[2]['fromislno'], 'dep')] = in_edge[2]['departuretime']
    
    for node in graph:
        for dep_node in dep_node_dict[node].keys():
            expanded_graph.add_edge((node, '0', -1, 'start'), dep_node, time=0)
            for arr_node in arr_node_dict[node].keys():
                expanded_graph.add_edge(arr_node, dep_node, time = calculate_time(arr_node_dict[node][arr_node], dep_node_dict[node][dep_node]).seconds)
        for arr_node in arr_node_dict[node].keys():
            expanded_graph.add_edge(arr_node, (node, '0', -1, 'end'), time=0)
            
    return expanded_graph
