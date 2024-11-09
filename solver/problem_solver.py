# Parses problems.csv and solves them
import pandas as pd
import csv


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
