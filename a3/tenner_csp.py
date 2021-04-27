#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools
####helper function
def get_array(board,x,y,x_range,y_range):
    variables = []
    for i in board[x][y].domain():
        for j in board[x_range][y_range].domain():
            if i != j:
                variables.append((i, j))
    return variables
    
def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return
       tenner_csp_model, variable_array
       where tenner_csp_model is a csp representing board grid using model_1
       and variable_array is a list of lists
       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]
       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n row, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
    
    row = len(initial_tenner_board[0])
    col = 10
    board = [[0 for x in range(col)] for y in range(row)]
    
    for i in range(row):
        for j in range(col):
            if initial_tenner_board[0][i][j] == -1:
                board[i][j] = Variable("V{}{}".format(i, j), [0,1,2,3,4,5,6,7,8,9])
            if initial_tenner_board[0][i][j] != -1:
                board[i][j] = Variable("V{}{}".format(i, j), [initial_tenner_board[0][i][j]])


    tenner_csp_model  = CSP("tenner_model_1", [board[x][y] for x in range(row) for y in range(col)])
    
    # contiguous constraints - up,down and diagonal adjacent
    con_diaup = []
    con_diadown = []
    con_col = []
    for x in range(row-1):
        for y in range(col):
        # diagonal constraints
            if y != col-1:
                con_diaup = Constraint("Diagonal_up", [board[x][y], board[x + 1][y + 1]])
                variables = get_array(board,x,y,x + 1,y + 1)
                con_diaup.add_satisfying_tuples(variables)
                tenner_csp_model.add_constraint(con_diaup)

            if y != 0:
                con_diadown = Constraint("Diagonal_down", [board[x][y], board[x + 1][y - 1]])
                variables = get_array(board,x,y,x + 1,y - 1)
                con_diadown.add_satisfying_tuples(variables)
                tenner_csp_model.add_constraint(con_diadown)
            # up/dowwn   
            con_col = Constraint("column", [board[x][y], board[x + 1][y]])
            variables = get_array(board,x,y,x + 1,y)
            con_col.add_satisfying_tuples(variables)
            tenner_csp_model.add_constraint(con_col)
    
    # row constraints
    con_row = []
    for x in range(row):
        for y in range(col):
            for z in range(y + 1, col):  
                con_row = Constraint("row", [board[x][y], board[x][z]]) 
                variables = get_array(board,x,y,x,z)
                con_row.add_satisfying_tuples(variables)
                tenner_csp_model.add_constraint(con_row)    

           

    # sum constraints
    con_sum = []
    for y in range(col):
        scope = []
        domain = []
        variables_sum = []
       
        for x in range(row):
            scope += [board[x][y]]
            domain = [board[x][y].cur_domain() for x in range(row)]
        
        con_sum = Constraint("sum" + str(y), scope)

        for t in itertools.product(*domain):
            if sum(t) == (initial_tenner_board[1])[y]: 
                variables_sum += [t[:row]]

        con_sum.add_satisfying_tuples(variables_sum)
        tenner_csp_model.add_constraint(con_sum)
    
    #tenner_csp_model.add_constraint(con_diaup)
    #tenner_csp_model.add_constraint(con_diadown)
    #tenner_csp_model.add_constraint(con_col)
    #tenner_csp_model.add_constraint(con_row)    
    #tenner_csp_model.add_constraint(con_sum)
    return tenner_csp_model, board
##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return
       tenner_csp, variable_array
       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists
       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]
       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 7.


       The input board is specified as a pair (n_grid, last_row).
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid.
       If a -1 is in the list it represents an empty cell.
       Otherwise if a number between 0--9 is in the list then this represents a
       pre-set board position. E.g., the board

       ---------------------
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists

       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]


       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.

       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each
       column.
    '''
   
    row = len(initial_tenner_board[0])
    col = 10
    board = [[0 for x in range(col)] for y in range(row)]
    vars = []
    
    for i in range(row):
        v = [] 
        for j in range(col):
            if initial_tenner_board[0][i][j] == -1:
                board[i][j] = Variable("V{}{}".format(i, j), [0,1,2,3,4,5,6,7,8,9])
            if initial_tenner_board[0][i][j] != -1:
                board[i][j] = Variable("V{}{}".format(i, j), [initial_tenner_board[0][i][j]])
           


    tenner_csp_model  = CSP("tenner_model_2", [board[x][y] for x in range(row) for y in range(col)])
    
    # contiguous constraints - up,down and diagonal adjacent
    con_diaup = []
    con_diadown = []
    con_col = []
    for x in range(row-1):
        for y in range(col):
        # diagonal constraints
            if y != col-1:
                con_diaup = Constraint("Diagonal_up", [board[x][y], board[x + 1][y + 1]])
                variables = get_array(board,x,y,x + 1,y + 1)
                con_diaup.add_satisfying_tuples(variables)
                tenner_csp_model.add_constraint(con_diaup)

            if y != 0:
                con_diadown = Constraint("Diagonal_down", [board[x][y], board[x + 1][y - 1]])
                variables = get_array(board,x,y,x + 1,y - 1)
                con_diadown.add_satisfying_tuples(variables)
                tenner_csp_model.add_constraint(con_diadown)
            # up/dowwn   
            con_col = Constraint("column", [board[x][y], board[x + 1][y]])
            variables = get_array(board,x,y,x + 1,y)
            con_col.add_satisfying_tuples(variables)
            tenner_csp_model.add_constraint(con_col)
    
   # row constraints
    con_row=[]
    for x in range(row):
        scope = []
        index = []
        variables_row = []
        for y in range(col):
            scope += [board[x][y]]
            if initial_tenner_board[0][x][y] != -1:
                index += [y]
            elif initial_tenner_board[0][x][y] == -1:
                continue
        
        for t in itertools.permutations(range(col)):   
            for i in index:
                if t[i] != initial_tenner_board[0][x][i]:
                    break
                if t[i] == initial_tenner_board[0][x][i]:
                    variables_row += [t]
        con_row = Constraint('row'+str(x), scope)
        con_row.add_satisfying_tuples(variables_row)
        tenner_csp_model.add_constraint(con_row)


    # sum constraints
    con_sum = []
    for y in range(col):
        scope = []
        domain = []
        variables_sum = []
       
        for x in range(row):
            scope += [board[x][y]]
            domain = [board[x][y].cur_domain() for x in range(row)]
        
        con_sum = Constraint("sum" + str(y), scope)

        for t in itertools.product(*domain):
            if sum(t) == (initial_tenner_board[1])[y]: 
                variables_sum += [t[:row]]

        con_sum.add_satisfying_tuples(variables_sum)
        tenner_csp_model.add_constraint(con_sum)
    
    #tenner_csp_model.add_constraint(con_diaup)
    #tenner_csp_model.add_constraint(con_diadown)
    #tenner_csp_model.add_constraint(con_col)
    #tenner_csp_model.add_constraint(con_row)    
    #tenner_csp_model.add_constraint(con_sum)
    return tenner_csp_model, board