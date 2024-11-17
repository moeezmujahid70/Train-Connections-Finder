import heapq
from solver.problem_solver import construct_connection, construct_connection_expanded_graph
from solver.utils import add_seconds_to_time


def solve_cost_function(graph, start, target, schedule_df, cost_attribute='stops', input_arrival_time='00:00:00'):
    """
    Solves for the optimal path based on the specified cost attribute and formats the solution.
    """
    if cost_attribute == 'stops' or cost_attribute == 'timeintrain':
        station_sequence, train_sequence, total_cost = dijkstra_path(
            graph, start, target, cost_attribute)
        if station_sequence is None:
            return 'PATH NOT FOUND'
        connection = construct_connection(
            schedule_df, station_sequence, train_sequence)
    elif cost_attribute == 'traveltime':
        node_sequence, total_cost = dijkstra_path_expanded_graph(
            graph, start, target)
        if node_sequence is None:
            return 'PATH NOT FOUND'
        connection = construct_connection_expanded_graph(node_sequence)
    elif cost_attribute == 'arrivaltime':
        node_sequence, total_cost = dijkstra_path_expanded_graph(
            graph, start, target)
        if node_sequence is None:
            return 'PATH NOT FOUND'
        connection = construct_connection_expanded_graph(node_sequence)
        total_cost = add_seconds_to_time(input_arrival_time, total_cost)

    else:
        return 'Invalid Cost Attribute'

    return connection, str(total_cost)


def dijkstra_path(graph, start, target, cost_attribute):
    """
    Dijkstra's algorithm to find the shortest path in a MultiDiGraph.

    Parameters:
        graph (nx.MultiDiGraph): The graph to search.
        start (str): The starting node.
        target (str): The target node.
        cost_attribute (str): The edge attribute to use as the cost ('stops' or 'timeintrain').

    Returns:
        tuple: (station_sequence, train_sequence, total_cost)
    """
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

        # Skip if cost is already outdated
        if current_cost > costs[current_node] or current_node == target:
            continue

        # Check all edges to neighbors of the current node
        for neighbor, edges in graph[current_node].items():
            for _, attribute in edges.items():  # Handle multiple edges between nodes
                travel_cost = current_cost + attribute[cost_attribute]

                # Only update if this path is shorter
                if travel_cost < costs[neighbor]:
                    costs[neighbor] = travel_cost
                    predecessors[neighbor] = {
                        'previous_station': current_node,
                        'train': attribute['train']
                    }
                    heapq.heappush(priority_queue, (travel_cost, neighbor))

    # If we reach the target node, reconstruct the path
    if predecessors[target]['train'] is not None:
        # Reconstruct the optimal path
        current_node = target
        station_sequence = []
        train_sequence = []
        while current_node is not None:
            station_sequence.append(current_node)
            if predecessors[current_node]['train'] is not None:
                train_sequence.append(predecessors[current_node]['train'])
            current_node = predecessors[current_node]['previous_station']
        return station_sequence[::-1], train_sequence[::-1], costs[target]

    # Return if target is unreachable
    return None, None, None


def dijkstra_path_expanded_graph(graph, start, target):
    """
    Dijkstra's algorithm to find the shortest path in a MultiDiGraph.

    Parameters:
        graph (nx.MultiDiGraph): The graph to search.
        start (str): The starting node.
        target (str): The target node.
        cost_attribute (str): The edge attribute to use as the cost ('stops' or 'timeintrain').

    Returns:
        tuple: (station_sequence, train_sequence, total_cost)
    """
    start = (start, '0', -1, 'start')
    target = (target, '0', -1, 'end')
    # Initialize costs to infinity and set the start node cost to 0
    costs = {node: float('infinity') for node in graph}
    costs[start] = 0

    # Dictionary to store the predecessor of each node to reconstruct the path
    predecessors = {node: None for node in graph}
    costs_from_pred = {node: None for node in graph}

    # Priority queue to keep track of nodes to visit
    priority_queue = [(0, start)]  # (current_cost, current_node)

    while priority_queue:
        # Get the node with the smallest cost
        current_cost, current_node = heapq.heappop(priority_queue)

        # Skip if cost is already outdated
        if current_cost > costs[current_node] or current_node == target:
            continue

        # Check all edges to neighbors of the current node
        for neighbor, attribute in graph[current_node].items():
            travel_cost = current_cost + attribute['time']

            # Only update if this path is shorter
            if travel_cost < costs[neighbor]:
                costs[neighbor] = travel_cost
                predecessors[neighbor] = current_node
                costs_from_pred[neighbor] = attribute['time']
                heapq.heappush(priority_queue, (travel_cost, neighbor))

    # If we reach the target node, reconstruct the path
    if predecessors[target] is not None:
        # Reconstruct the optimal path
        current_node = target
        node_sequence = []
        while current_node is not None:
            node_sequence.append(current_node)
            current_node = predecessors[current_node]

        return node_sequence[::-1], costs[target]

    # Return if target is unreachable
    return None, None
