# Linear Programming Solver

A comprehensive Python application for solving linear programming optimization problems with an intuitive graphical user interface built using Flet. This tool is designed to help users maximize or minimize objective functions subject to linear constraints, making it ideal for production optimization, resource allocation, and other operational research scenarios.

## Overview

This application implements the Simplex algorithm to solve linear programming problems. Users can input their objective function coefficients and constraint matrices through a modern, cross-platform GUI. The solver computes the optimal solution and displays the step-by-step iterations of the Simplex method, along with a clear interpretation of the results.

The app is specifically tailored for production optimization problems, where businesses need to determine the optimal production quantities for different products given limited resources and profit margins.

## Features

- **Simplex Algorithm Implementation**: Efficient implementation of the Simplex method for solving linear programming problems
- **Interactive GUI**: Built with Flet for a responsive, cross-platform user interface
- **Dynamic Problem Input**: Users can specify the number of variables and constraints dynamically
- **Step-by-Step Solution Display**: Visualizes each iteration of the Simplex algorithm in tabular form
- **Optimal Solution Interpretation**: Provides clear, business-friendly explanations of the results
- **Theme Support**: Light and dark mode toggle for user preference
- **Error Handling**: Robust input validation and error messages
- **Production Optimization Focus**: Specialized for manufacturing and production planning scenarios

## Requirements

- Python 3.8 or higher
- Flet (for GUI)
- NumPy (for numerical computations)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DrBider-dev/IO-Project.git
cd IO-Project
```

2. Install dependencies:
```bash
pip install flet numpy
```

Alternatively, create a `requirements.txt` file with the following content:
```
flet>=0.21.0
numpy>=1.21.0
```

Then install:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. In the GUI:
   - Enter the number of decision variables (products) and constraints (resource limitations)
   - Click the settings icon to generate the input form
   - Fill in the objective function coefficients (contribution margins for each product)
   - Enter the constraint matrix (resource requirements for each product and constraint)
   - Click "Calcular Solución" to solve the problem

3. View the results:
   - Step-by-step Simplex table iterations
   - Final optimal production quantities for each product
   - Maximum profit estimate

## Project Structure

```
IO-Project/
├── main.py                 # Main application file with GUI logic
├── README.md               # This file
├── data/                   # Directory for data files (if any)
├── solver/
│   └── simplex_engine.py   # Simplex algorithm implementation
└── ui/
    └── components.py       # UI components and styling
└── utils/                  # Utility functions (if any)
```

### Key Files Description

- **main.py**: The entry point of the application. Contains the Flet page setup, event handlers, and the main logic for user interaction.
- **solver/simplex_engine.py**: Implements the SimplexSolver class with the `resolver` method that performs the Simplex algorithm iterations.
- **ui/components.py**: Defines UI styling constants and reusable components like headers and cards.

## How It Works

The application uses the Simplex method, a popular algorithm for solving linear programming problems:

1. **Problem Formulation**: Users input the objective function coefficients (c), constraint matrix (A), and right-hand side values (b).

2. **Initial Tableau**: The solver constructs the initial Simplex tableau with the constraint matrix, slack variables, and objective function.

3. **Iterations**: The algorithm iteratively improves the solution by:
   - Selecting the entering variable (most negative coefficient in objective row)
   - Choosing the leaving variable (minimum ratio test)
   - Performing pivot operations to update the tableau

4. **Optimality Check**: Continues until all coefficients in the objective row are non-negative.

5. **Result Interpretation**: Extracts the optimal values for decision variables and objective function value.

The GUI displays each iteration table and provides a user-friendly summary of the optimal production plan.

## Example

For a furniture manufacturing company producing tables, chairs, bookshelves, and desks with limited wood, labor, and machine time:

- **Objective**: Maximize profit: 200*X1 + 150*X2 + 180*X3 + 220*X4
- **Constraints**: Wood ≤ 1000, Labor ≤ 800, Machine ≤ 600, etc.

The app will compute the optimal production quantities for each product type.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## More Stuff

Document:https://docs.google.com/document/d/1Ry2sEIA5kxxWDe7Zf91vtLFVA-1dihvGiq8kAtWoyt8/edit?tab=t.0

## Author

Brayan Estiven Aguirre Aristizabal - Universidad Distrital