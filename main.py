from solver.problem_solver import load_problems_csv, read_and_preprocess_csv, solve_cost_stop, create_solutions_csv
from solver.graph_builder import build_graph
import pandas as pd

def main():
    
    problems_file = "problems/example-problems.csv"
    mini_schedule_file = "data/mini-schedule.csv"  
    schedule_file = "data/schedule.csv"         # File containing schedule data

    # Load and preprocess the problem
    problems_df = load_problems_csv(problems_file)
    mini_schedule_df = read_and_preprocess_csv(mini_schedule_file)
    schedule_df = read_and_preprocess_csv(schedule_file)
    print(mini_schedule_df.head())
    print(schedule_df.head())
    print(problems_df.head())
    # build Graph from data
    graph = build_graph(schedule_df)
    mini_graph = build_graph(mini_schedule_df)
    rslt_df = problems_df.loc[(problems_df['CostFunction'] == 'stops')]# & (problems_df['Schedule'] == 'mini-schedule.csv')]
    solutions = {'ProblemNo':[],'Connection':[],'Cost':[]}
    for _, row in rslt_df.iterrows():
        if row['Schedule'] == 'mini-schedule.csv':
            df = mini_schedule_df
            G = mini_graph
        else:
            df = schedule_df
            G = graph
        connection, cost = solve_cost_stop(G, row['FromStation'], row['ToStation'], df)
        solutions['ProblemNo'].append(row['ProblemNo'])
        solutions['Connection'].append(connection)
        solutions['Cost'].append(cost)
    create_solutions_csv(solutions, 'solutions/my-example-solutions.csv')
    
    
    
        
    

if __name__ == "__main__":
    main()
