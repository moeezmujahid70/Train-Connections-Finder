# Repository for ws2425.1.1/team301

**Topic:** WS24/25 Assignment 1.1: Find Train Connections

# Find Train Connections

## Project Description

The **Find Train Connections** project is designed to process and solve transportation scheduling problems using graph-based algorithms. It takes input data in the form of schedules and problem definitions, builds an expanded graph representation of the schedule, and applies various cost functions to find optimal solutions for problems such as minimizing stops, travel time, or arrival delays.

---

## Table of Contents
1. [Dependencies](#dependencies)
2. [How to Run the Code](#how-to-run-the-code)
3. [Repository Structure](#repository-structure)

---

## Dependencies

### Programming Language and Version
- **Python**: 3.10+

### External Libraries
The following external libraries are required to run the code:

- `pandas`: For data manipulation and CSV file handling.
- `networkx`: For graph operations and algorithms.
- `numpy`: For numerical operations.
- `matplotlib` (optional): For visualizing graphs or results.

#### Installing Dependencies
To install the required libraries, use the following command:

```bash
pip install -r requirements.txt
```


## How to Run the Code

1.	Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/problem-solver.git
```

2.	Run the Main Script
Execute the 
```bash
python main.py
```

3.	Output
The solutions will be saved in the solutions/ directory

4.	Solve Custom Problems
To solve other problems:
	-	Add your problem definitions to problems/problems.csv.
	-	Ensure corresponding schedule files (mini-schedule.csv or schedule.csv) are placed in the data/ folder.
	-	Run main.py as described above.


## Repository Structure

ROOT/
├── data/
│   ├── mini-schedule.csv        # mini schedule data
│   ├── schedule.csv             # Full schedule data
│   ├── problems.csv             # Problem definitions
├── solutions/
│   └── solutions.csv  # Output solutions
├── solver/
│   ├── __init__.py              # Package initialization
│   ├── problem_solver.py        # Functions for loading and processing problems
│   ├── costFuntions.py          # Cost function implementations
│   ├── graph_builder.py         # Functions for building and expanding graphs
│   └── utils.py                 # Utility functions (e.g., time calculation)
├── main.py                      # Main script to run the solver
├── requirements.txt             # List of dependencies
└── README.md                    # This file