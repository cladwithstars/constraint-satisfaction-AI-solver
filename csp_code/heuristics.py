#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import operator
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    #IMPLEMENT
    return sorted(csp.get_all_unasgn_vars(), key=lambda x: x.cur_domain_size())[0]

def val_lcv(csp,var):
    
    
    curr = list()
    
    for con in csp.get_cons_with_var(var):
        for val in var.cur_domain():
            var.assign(val)
            sizeDom = sum([con.has_support(v, d) for v in con.get_unasgn_vars() for d in v.cur_domain()])
            var.unassign()
            
            if val not in [x[0] for x in curr]:
                curr.append((val, sizeDom))
                        
                
    vals = sorted(curr, key=lambda x: x[1])[::-1]
           
    return [vals[i][0] for i in range(len(vals))] 
    