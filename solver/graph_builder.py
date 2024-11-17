from collections import defaultdict
from solver.utils import calculate_time_differenc
import pandas as pd
import networkx as nx


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
            travel_time_seconds = calculate_time_differenc(
                group.iloc[i]['Departure time'], group.iloc[i + 1]['Arrival time']).seconds

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
    """
    Expands a MultiDiGraph to capture detailed arrival and departure times at stations.
    """
    expanded_graph = nx.DiGraph()
    arr_node_dict = defaultdict(dict)
    dep_node_dict = defaultdict(dict)

    # Add edges between arrival and departure nodes
    for node in graph:
        for in_edge in graph.in_edges(node, data=True):
            dep_node = (in_edge[0], in_edge[2]['train'],
                        in_edge[2]['fromislno'], 'dep')
            arr_node = (node, in_edge[2]['train'],
                        in_edge[2]['toislno'], 'arr')

            # Add edge to expanded graph with departure time as an attribute
            expanded_graph.add_edge(
                dep_node,
                arr_node,
                time=in_edge[2]['timeintrain'],
                departuretime=in_edge[2]['departuretime']
            )

            # Store arrival and departure times in dictionaries
            arr_node_dict[node][arr_node] = in_edge[2]['arrivaltime']
            dep_node_dict[in_edge[0]][dep_node] = in_edge[2]['departuretime']

    # Ensure every station has virtual start and end connections
    all_nodes = set(graph.nodes())

    for node in all_nodes:
        dep_nodes = dep_node_dict.get(node, {})
        arr_nodes = arr_node_dict.get(node, {})

        # Connect virtual start to all departure nodes
        for dep_node, dep_time in dep_nodes.items():
            expanded_graph.add_edge(
                (node, '0', -1, 'start'),
                dep_node,
                time=0,
                departuretime=dep_time
            )

        # Connect all arrival nodes to virtual end
        for arr_node in arr_nodes:
            expanded_graph.add_edge(arr_node, (node, '0', -1, 'end'), time=0)

        # Connect all arrival nodes to departure nodes within the same station
        for arr_node, arr_time in arr_nodes.items():
            for dep_node, dep_time in dep_nodes.items():
                time_spent = calculate_time_differenc(
                    arr_time, dep_time).seconds
                expanded_graph.add_edge(arr_node, dep_node, time=time_spent)

    return expanded_graph
