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


def build_graph(schedule_df: pd.DataFrame) -> nx.DiGraph:
    """
    Builds a directed graph from the schedule data using NetworkX, adding timeintrain.
    """
    G = nx.DiGraph()  # Directed graph

    # Group by train number to handle consecutive stops for each train
    for train_no, group in schedule_df.groupby('Train No.'):
        group = group.sort_values('islno')  # Sort by stop order (islno)

        # Iterate through consecutive stops for each train
        for i in range(len(group) - 1):
            from_station = group.iloc[i]['station Code']
            to_station = group.iloc[i + 1]['station Code']

            # Calculate travel time in seconds
            travel_time_seconds = calculate_travel_time(
                group.iloc[i],  group.iloc[i + 1]).seconds

            # Add a directed edge from from_station to to_station with default weight and timeintrain
            G.add_edge(
                from_station,
                to_station,
                train=train_no,
                weight=1,  # Default weight (costFuntion:Stops)
                timeintrain=travel_time_seconds  # Add time spent in the train
            )

    return G
