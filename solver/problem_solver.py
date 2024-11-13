import pandas as pd
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


def construct_connection(schedule_df, station_sequence, train_sequence):
    """
    Constructs the formatted connection string from station and train sequences.
    """
    identical_train_groups = [list(y) for _, y in groupby(train_sequence)]

    station_seq = [station_sequence[0]]
    counter = 0
    for identical_train_group in identical_train_groups:
        counter += len(identical_train_group)
        station_seq.append(station_sequence[counter])

    train_seq = []
    for identical_train_group in identical_train_groups:
        train_seq += list(set(identical_train_group))

    # Construct the connection string
    connection = []
    for i in range(len(train_seq)):
        train_no = train_seq[i].strip()
        start_station = station_seq[i]
        end_station = station_seq[i + 1]

        # Fetch islno for both stations
        start_islno = schedule_df[(schedule_df['Train No.'] == train_no) &
                                  (schedule_df['station Code'] == start_station)]['islno'].values[0]
        end_islno = schedule_df[(schedule_df['Train No.'] == train_no) &
                                (schedule_df['station Code'] == end_station)]['islno'].values[0]

        # Append formatted result
        connection.append(f"{train_no} : {start_islno} -> {end_islno}")

    return ' ; '.join(connection)


def create_solutions_csv(solutions: dict, filepath: str):
    """
    Generates a solutions CSV file.
    """
    try:
        solutions_df = pd.DataFrame(solutions)
        solutions_df.to_csv(filepath, index=False)
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
