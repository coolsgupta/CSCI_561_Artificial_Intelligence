# CSCI_561_Artificial_Intelligence Assignment 1

## Notes

### Actions

#### Straight Moves 
     X+    :  1
     X-    :  2
     Y+    :  3
     Y-    :  4 
     Z+    :  5 
     Z-    :  6 

#### Diagonal Moves
     X+Y+  :  7
     X+Y-  :  8
     X-Y+  :  9
     X-Y-  :  10
     X+Z+  :  11
     X+Z-  :  12
     X-Z+  :  13
     X-Z-  :  14
     Y+Z+  :  15
     Y+Z-  :  16
     Y-Z+  :  17
     Y-Z-  :  18

### Arguments
    
    No Command line arguments

### Input and Output
    
    Working Directory : Same as script
    Read File : input.txt
    Write File: output.txt
    
#### Input Format

    Input: The file input.txt in the current directory of your program will be formatted as follows:
    
    First line: Instruction of which algorithm to use, as a string: BFS, UCS or A*
    
    Second line: Three strictly positive 32-bit integers separated by one space
    character, for the size of X, Y, and Z dimensions, respectively.
    
    Third line: Three non-negative 32-bit integers for the entrance grid location.
    
    Fourth line: Three non-negative 32-bit integers for the exit grid location.
    
    Fifth line: A strictly positive 32-bit integer N, indicating the number of grids in the
    maze where there are actions available.
    Next N lines: Three non-negative 32-bit integers separated by one space character, for
    the location of the grid, followed by a list of actions that are available at
    this grid. The grid location is guaranteed to be legal and within the maze.

#### Output Format
    
    First line: A single integer C, indicating the total cost of your found solution. If no
    solution was found (the exit grid location is unreachable from the given entrance, then
    write the word “FAIL” (all capital) without any other lines following.
    
    Second line: A single integer N, indicating the total number of steps in your solution
    including the starting position.
    
    N lines: Report the steps in your solution travelling from the entrance grid
    location to the exit grid location as were given in the input.txt file.
        Write out one line per step with cost. Each line should contain a
        tuple of four integers: X, Y, Z, Cost, separated by a space
        character, specifying the grid location with the single step cost to
        visit that grid location by your agent from its last grid during its
        traveling from the entrance to the exit
        
### Notes
    
    Name of program : “homework3.py”.
    
    