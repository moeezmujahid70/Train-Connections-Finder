from solver.problem_solver import load_problems_csv, read_and_preprocess_csv, create_solutions_csv
from solver.costFunctions import solve_cost_function
from solver.graph_builder import build_graph, expand_graph, adjust_start_times


def main():

    problems_file = "problems/problems.csv"
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

    solutions = {'ProblemNo': [], 'Connection': [], 'Cost': []}

    cost_functions = [
        ('stops', mini_graph, graph),
        ('timeintrain', mini_graph, graph),
        ('arrivaltime', expanded_mini_graph, expanded_graph),
        ('traveltime', expanded_mini_graph, expanded_graph)
    ]

    # Iterate through all problems
    for cost_function, mini_g, full_g in cost_functions:
        rslt_df = problems_df.loc[(
            problems_df['CostFunction'] == cost_function)]

        for _, row in rslt_df.iterrows():
            if row['Schedule'] == 'mini-schedule.csv':
                df = mini_schedule_df
                G = mini_g
            else:
                df = schedule_df
                G = full_g

            if cost_function == 'arrivaltime':
                G = adjust_start_times(
                    G, row['FromStation'], row['input_time'])
                connection, cost = solve_cost_function(
                    G, row['FromStation'], row['ToStation'], df, cost_function, row['input_time']
                )
            else:
                connection, cost = solve_cost_function(
                    G, row['FromStation'], row['ToStation'], df, cost_function
                )

            solutions['ProblemNo'].append(row['ProblemNo'])
            solutions['Connection'].append(connection)
            solutions['Cost'].append(cost)

    create_solutions_csv(solutions, 'solutions/solutions.csv')


if __name__ == "__main__":
    main()
