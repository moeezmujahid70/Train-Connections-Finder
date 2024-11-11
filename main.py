from solver.problem_solver import load_problems_csv, read_and_preprocess_csv, solve_cost_stop
from solver.graph_builder import build_graph

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
    print(solve_cost_stop(graph, 'TK', 'SGD', schedule_df))
        
    

if __name__ == "__main__":
    main()
