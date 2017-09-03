# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Solving the naked twins within a unit using constraint propagation requires identifying the twins and then removing their values as possibilities from the non-twins.  

One implementation approach is to loop through the units for boxes that have a length of probable values equaling two.  If another box shares these and only these same values, the two boxes are considered naked twins.  The remainder of the algorithm is implemented by covering the non-twins within the same unit and removing the twin's values from the non-twins list of probable values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propagation solves the diagonal sudoku puzzles through three algorithms.  The first is the elimination of single values from all its peers.   The second is extracts the values that are the only choice for a given box.  The third used naked twins within a unit of peers to remove cumulative probabilities of 100% from the remaining boxes in that unit.  Finally, a depth first search is used to branch on the minimum length boxes, instancing a parallel copy of the game with the range of possible guesses, until it finds the correct solution.  

Appending the diagonals to the list of units and peers was straight forward.  This way, while implementing constraint propagation, diagonals are treated the same as any other unit. 

A minor modification was needed to the depth first search, only choice, naked twins, and eliminate function definitions to complete the diagonal sudoku implementation.  

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

