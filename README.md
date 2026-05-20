# Linear Programming Solver

A comprehensive Python application for solving linear programming optimization problems with an intuitive graphical user interface built using Flet. This tool is designed to help users maximize or minimize objective functions subject to linear constraints, making it ideal for production optimization, resource allocation, and other operational research scenarios.

## Overview

This application implements the Simplex algorithm to solve linear programming problems. Users can input their objective function coefficients and constraint matrices through a modern, cross-platform GUI. The solver computes the optimal solution and displays the step-by-step iterations of the Simplex method, along with a clear interpretation of the results.

The app is specifically tailored for production optimization problems, where businesses need to determine the optimal production quantities for different products given limited resources and profit margins.

## Features

- **Simplex Algorithm Implementation**: Efficient implementation of the Simplex method and two-phases method for solving linear programming problems
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
2. Create and activate virtual env:
```bash
python -m venv venv
# Windows (CMD): venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```
3. Install:
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
├── main.py                 # Application entry point and Flet initialization
├── requirements.txt        # Project dependencies (flet, numpy)
├── .gitignore              # Files and folders excluded from version control
├── IO.mp4                  # Demo video showing the application in action
├── solver/
│   ├── simplex_engine.py   # Classic Simplex method implementation using NumPy
│   ├── twoPhases_engine.py # Two-Phases method implementation using NumPy
│   └── solver_wrapper.py   # Wrapper to select and execute the appropriate method
└── ui/
    ├── components.py       # Generic visual components and Flet styles
    ├── input_form.py       # Dynamic form for entering variables and constraints
    ├── results_display.py  # Main view for displaying the optimal solution
    └── table_renderer.py   # Step-by-step rendering of the iterative simplex tableaux
```

## How It Works

The application uses the Simplex or two-phases method, two popular algorithms for solving linear programming problems:

1. **Problem Formulation**: Users input the objective function coefficients (c), constraint matrix (A), and right-hand side values (b).

2. **Initial Tableau**: The solver constructs the initial Simplex tableau with the constraint matrix, slack variables, and objective function.

3. **Iterations**: The algorithm iteratively improves the solution by:
   - Selecting the entering variable (most negative coefficient in objective row)
   - Choosing the leaving variable (minimum ratio test)
   - Performing pivot operations to update the tableau

4. **Optimality Check**: Continues until all coefficients in the objective row are non-negative.

5. **Result Interpretation**: Extracts the optimal values for decision variables and objective function value.

The GUI displays each iteration table and provides a user-friendly summary of the optimal production plan.

## Author

Brayan Estiven Aguirre Aristizabal(20231020156) - Universidad Distrital