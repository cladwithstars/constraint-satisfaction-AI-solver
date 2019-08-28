#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools

def binary_ne_grid(kenken_grid):
    ##IMPLEMENT
    size = kenken_grid[0][0] #size of each dim of the board
    dim = range(1, size + 1)
    vals = [x for x in dim] # the domain
    cons= [] #the constraints that we will build
    
    rows = list() #list of list, this represents the board
    
    
    for r in dim: #add the vars to the rows list
        rows.append([Variable('V' + str(r) + str(c), vals) for c in dim])
        
    cols = [] #the columns
    for i in range(size):
        cols.append([rows[j][i] for j in range(size)])    
    
    colCons = getBoardCons(cols, 2, vals)
    for c in colCons:
        cons.append(c)
    
    rowCons = getBoardCons(rows, 2, vals)
    for r in rowCons:
        cons.append(r)    
        
    #now construct the CSP from all the variables and constraints we have
    cspName = str(size) + 'x' + str(size) + ' binary_ne_grid'
    cspVars = [var for row in rows for var in row]
    
    csp = CSP(cspName, cspVars)
    
    for con in cons:
        csp.add_constraint(con)    
    
    return csp, rows
    
            
def nary_ad_grid(kenken_grid):
    ##IMPLEMENT 
    size = kenken_grid[0][0] #size of each dim of the board
    dim = range(1, size + 1)
    vals = [x for x in dim] # the domain
    
    rows = list() #list of list, this represents the board
    cons= [] 
    
    for r in dim:
        rows.append([Variable('V' + str(r) + str(c), vals) for c in dim])
    
    cols = [] #the columns
    for i in range(size):
        cols.append([rows[j][i] for j in range(size)])    
    
    colCons = getBoardCons(cols, size, vals)
    for c in colCons:
        cons.append(c)
    
    rowCons = getBoardCons(rows, size, vals)
    for r in rowCons:
        cons.append(r)       
    
    #now construct the CSP from all the variables we have
    cspName = str(size) + 'x' + str(size) + ' binary_ne_grid'
    cspVars = [var for row in rows for var in row]
    
    csp = CSP(cspName, cspVars)
    for con in cons:
        csp.add_constraint(con)
    
    
    return csp, rows

######################## 
#Below are helper functions for the cage constraints for kenken_csp_model
#######################

def subConstraint(l, targ):
    def subtractAll(l):
        return l[0] - sum(l[1:])
    for perm in itertools.permutations(l):
        if subtractAll(perm) == targ:
            return True
    return False


   
def multConstraint(l, targ):
    curr = 1
    for num in l:
        curr*=num
    
    return curr == targ

def divConstraint(l, targ):
    def divideAll(l):
        mult = 1
        for num in l[1:]:
            mult*= num
        div = l[0] / mult 
        return div
    for perm in itertools.permutations(l):
        if divideAll(perm) == targ:
            return True
    return False

def getCageCons(L, size, operation, target):
    '''get the satisfying tuples for a cage constraint'''
    satisfyingTuples = []
    prod = itertools.product(L, repeat = size)
    
    for p in prod:
    
        if operation == 0 and sum(p) == target: 
            satisfyingTuples.append(p)
        elif operation == 1 and subConstraint(p, target):
            satisfyingTuples.append(p)
        elif operation == 2 and divConstraint(p, target):
            satisfyingTuples.append(p)
        elif operation == 3 and multConstraint(p, target): 
            satisfyingTuples.append(p)
                
    return satisfyingTuples

def getBoardCons(cols, size, vals):
    '''get row or col cons'''
    cons = []
    
    tups = [t for t in itertools.permutations(vals, size)]
    for col in cols:
        for v in itertools.combinations(col, size):
            conName, scope = 'C' + str(list(v)), list(v) 
            con = Constraint(conName, scope)
            con.add_satisfying_tuples(tups)   
            cons.append(con)
    return cons
            
            

########################

########################

 
    
def kenken_csp_model(kenken_grid):
    ##IMPLEMENT
    
    
    size = kenken_grid[0][0] #size of each dim of the board
    dim = range(1, size + 1)
    vals = [x for x in dim] # the domain
    binTups = [t for t in itertools.permutations(vals, 2)]
    cons= [] #the constraints (to add)
    
    rows = list() #list of list, this represents the VARIABLES
    
    for r in dim:
        rows.append([Variable('V' + str(r) + str(c), vals) for c in dim])
    
    cols = [] #the columns
    for i in range(size):
        cols.append([rows[j][i] for j in range(size)])
    
    #first get row and column constraints and add to cons list
    #using binary constraints
    cons += [x for x in getBoardCons(cols, 2, vals)] + [y for y in getBoardCons(rows, 2, vals)]
    
               
    #now do cage constraints
    for c in kenken_grid[1:]:
        
        if len(c) == 2:
            #in this special case, we just have (cell, target) constraint
            targetVal = c[1]
            i = int(str(c[0])[0]) -1 
            j = int(str(c[0])[1]) -1 
            
            name = 'Val Enforce Cage constraint on V' + str(i) + str(j)
            con = Constraint(name, rows[i][j]) #second arg is the scope...
            con.add_satisfying_tuples([(targetVal)]) #is this right?
            cons.append(con)
            
        else:
            
            cageSize = len(c[:-2])
            target, operation = c[-2], c[-1] 
            
            scopeVals = [rows[int(str(c[val])[0]) - 1][int(str(c[val])[1]) -1] for val in range(cageSize)]
            
            con = Constraint(str(scopeVals), scopeVals)
            
            satisfyingTuples = getCageCons(vals, cageSize, operation, target)
            
            con.add_satisfying_tuples(satisfyingTuples)
            cons.append(con)
            
    
    cspName = str(size) + 'x' + str(size) + ' binary KenKen With Cage Constraints'
    cspVars = [var for row in rows for var in row] #flattening the list
        
    csp = CSP(cspName, cspVars)
    
    for con in cons:
        csp.add_constraint(con)    
    
    return csp, rows


    
        
        
                        
                    
            
                
            
            
            
            
        
    
