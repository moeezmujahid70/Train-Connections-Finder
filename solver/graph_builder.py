import pandas as pd
import networkx as nx


def build_graph(schedule_df: pd.DataFrame) -> nx.DiGraph:
    """
    Builds a directed graph from the schedule data using NetworkX.
    """
    G = nx.DiGraph()  # Directed graph

    # Group by train number to handle consecutive stops for each train
    for train_no, group in schedule_df.groupby('Train No.'):
        group = group.sort_values('islno')

        # Iterate through consecutive stops for each train
        for i in range(len(group) - 1):
            from_station = group.iloc[i]['station Code']
            to_station = group.iloc[i + 1]['station Code']

            # Add a directed edge from from_station to to_station
            G.add_edge(from_station, to_station, train=train_no, weight = 1)

    return G
