from solver.problem_solver import load_problems_csv, read_and_preprocess_csv, solve_cost_stop, create_solutions_csv
from solver.graph_builder import build_graph
import pandas as pd

def main():
    
    problems_file = "problems/example-problems.csv"
    schedule_file = "data/mini-schedule.csv"  # File containing schedule data

    # Load and preprocess the problem
    problems_df = load_problems_csv(problems_file)
    schedule_df = read_and_preprocess_csv(schedule_file)
    print(schedule_df.head())
    print(problems_df.head())
    # build Graph from data
    graph = build_graph(schedule_df)
    rslt_df = problems_df.loc[(problems_df['CostFunction'] == 'stops') & (problems_df['Schedule'] == 'mini-schedule.csv')]
    solutions = {'ProblemNo':[],'Connection':[],'Cost':[]}
    for _, row in rslt_df.iterrows():
        connection, cost = solve_cost_stop(graph, row['FromStation'], row['ToStation'], schedule_df)
        solutions['ProblemNo'].append(row['ProblemNo'])
        solutions['Connection'].append(connection)
        solutions['Cost'].append(cost)
    create_solutions_csv(solutions, 'solutions/my-example-solutions.csv')
    
    
    
        
    

if __name__ == "__main__":
    main()
