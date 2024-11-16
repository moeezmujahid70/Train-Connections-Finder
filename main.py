from solver.problem_solver import load_problems_csv, read_and_preprocess_csv, create_solutions_csv
from solver.costFuntions import solve_cost_funtion
from solver.graph_builder import build_graph, expand_graph


def main():

    problems_file = "problems/example-problems.csv"
    mini_schedule_file = "data/mini-schedule.csv"
    schedule_file = "data/schedule.csv"         # File containing schedule data

    # Load and preprocess the problem
    problems_df = load_problems_csv(problems_file)
    mini_schedule_df = read_and_preprocess_csv(mini_schedule_file)
    schedule_df = read_and_preprocess_csv(schedule_file)

    # build Graph from data
    graph = build_graph(schedule_df)
    mini_graph = build_graph(mini_schedule_df)
    expanded_mini_graph = expand_graph(mini_graph)
    expanded_graph = expand_graph(graph)
   # Display some edges with the new timeintrain attribute

    rslt_df = problems_df.loc[(problems_df['CostFunction'] == 'stops')]
    rslt_df_2 = problems_df.loc[(problems_df['CostFunction'] == 'timeintrain')]
    rslt_df_4 = problems_df.loc[(problems_df['CostFunction'] == 'traveltime')]
    solutions = {'ProblemNo': [], 'Connection': [], 'Cost': []}

    for _, row in rslt_df.iterrows():
        if row['Schedule'] == 'mini-schedule.csv':
            df = mini_schedule_df
            G = mini_graph
        else:
            df = schedule_df
            G = graph
        connection, cost = solve_cost_funtion(
            G, row['FromStation'], row['ToStation'], df, 'stops')
        solutions['ProblemNo'].append(row['ProblemNo'])
        solutions['Connection'].append(connection)
        solutions['Cost'].append(cost)

    for _, row in rslt_df_2.iterrows():
        if row['Schedule'] == 'mini-schedule.csv':
            df = mini_schedule_df
            G = mini_graph
        else:
            df = schedule_df
            G = graph
        connection, cost = solve_cost_funtion(
            G, row['FromStation'], row['ToStation'], df, 'timeintrain')
        solutions['ProblemNo'].append(row['ProblemNo'])
        solutions['Connection'].append(connection)
        solutions['Cost'].append(cost)
        
    for _, row in rslt_df_4.iterrows():
        if row['Schedule'] == 'mini-schedule.csv':
            df = mini_schedule_df
            G = expanded_mini_graph
        else:
            df = schedule_df
            G = expanded_graph
        connection, cost = solve_cost_funtion(
            G, row['FromStation'], row['ToStation'], df, 'traveltime')
        solutions['ProblemNo'].append(row['ProblemNo'])
        solutions['Connection'].append(connection)
        solutions['Cost'].append(cost)

    create_solutions_csv(solutions, 'solutions/my-example-solutions1.csv')


if __name__ == "__main__":
    main()
