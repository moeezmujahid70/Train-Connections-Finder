import pandas as pd
import networkx as nx
import csv


def load_problems_csv(problems_file_path) -> pd:
    '''
    loads and preprocess on problems csv
    '''
    problems_df = pd.read_csv(problems_file_path)
    problems_df[['CostFunction', 'time']] = problems_df['CostFunction'].str.split(
        ' ', expand=True)
    return problems_df


def read_and_preprocess_csv(schedule_file_path) -> pd:
    '''
    loads and preprocess on Dataset
    '''
    df = pd.read_csv(schedule_file_path)
    schedule_df = df.drop(['Destination Station Name', 'Destination station Code',
                          'Station Name', 'Destination Station Name'], axis=1)
    schedule_df['Train No.'] = schedule_df['Train No.'].str.strip("'")
    schedule_df['Arrival time'] = schedule_df['Arrival time'].str.strip("'")
    schedule_df['Departure time'] = schedule_df['Departure time'].str.strip(
        "'")
    schedule_df['station Code'] = schedule_df['station Code'].str.strip()
    return schedule_df
