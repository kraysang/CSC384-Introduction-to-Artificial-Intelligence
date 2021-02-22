#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems
'''new'''
import math


def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    #Manhattan Distance = abs(x1-x0) + abs (y1-y0)
    dist = 0
    for snowball in state.snowballs:
        dist += abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])
        
    return dist


#HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    #distance to be returned
    optimal_dist = 0
    man_dist = 0
    r_dist = []
  
    
    #given information
    h = state.height
    w = state.width
    top_left = (0, h)
    bottom_left = (0, 0)
    top_right = (w, h)
    bottom_right = (w, 0)
    
    #manhatten distance
    

    #check corner case
    for i in state.snowballs:
        if state.destination != i:
            
            #c1: check if it is in cornor
            if i == top_left or i == bottom_left or i == top_right or i == bottom_right:
                return float("inf")
            
            #c2:check if there is a wall, approve only if dest is at samne x&y axis of ball
            if (i[0] == 0 or i[0] == w-1) and state.destination[0] != i[0]:
                return float("inf")
            
            elif (i[1] == 0 or i[1] == h-1) and state.destination[1] != i[1]:
                return float("inf")
           
        
            #c3:if their are 2 obstacles cause a corner
        
            if (i[0]+1, i[1]) in state.obstacles:
                if (i[0],i[1]+1) in state.obstacles:
                    return float("inf")
            elif(i[0]-1, i[1]) in state.obstacles:
                if (i[0], i[1]-1) in state.obstacles:
                    return float("inf")
            elif(i[0]+1, i[1]) in state.obstacles:
                if(i[0], i[1]-1) in state.obstacles:
                    return float("inf")
            elif(i[0]-1, i[1]) in state.obstacles:
                if(i[0], i[1]+1) in state.obstacles:
                    return float("inf")
         
            
            #c4:if 1 obstacle cause corner with a wall
            if i[1] == 0 and (((i[0]-1,0)in state.obstacles) or ((i[0]+1,0)in state.obstacles)):
                return float("inf")
            elif i[1] == h-1 and (((i[0]-1,h-1)in state.obstacles) or ((i[0]+1,h-1)in state.obstacles)):
                return float("inf")
            elif i[0] == 0 and (((0,i[1]+1)in state.obstacles) or ((0,i[1]-1)in state.obstacles)):
                return float("inf")
            elif i[0] == w-1 and (((w-1,i[1]+1)in state.obstacles) or ((w-1,i[1]-1)in state.obstacles)):
                return float("inf")

            #c5:if some snow ball will be placed at destination
            if (state.snowballs[i] == 3 ) or (state.snowballs[i] == 4 ) or (state.snowballs[i] == 5):
                man_dist += 2*(abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1]))
            
            elif (state.snowballs[i]==6):
                man_dist += 3*(abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1]))
            
            elif (state.snowballs[i]==0):
                man_dist += 0.5*(abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1]))
            
            else:
                man_dist += (abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1]))
        
                
       
        elif i == state.destination:
            
            if state.snowballs[i] == 6:  
                return 0
            elif(state.snowballs[i] == 3 ) or (state.snowballs[i] == 0 ):
                man_dist += 0
            elif(state.snowballs[i] == 1 ) or (state.snowballs[i] == 2 ) or (state.snowballs[i] == 4) or (state.snowballs[i] == 5):
                man_dist += abs(state.destination[0] - state.robot[0]) + abs(state.destination[1] - state.robot[1])

        '''  
        #add some Euclidean distance
        if i == state.destination:
            #1.complete snow man on the goal
            #2.big snowball on the goal
            #3.medium and big snowball are stack on the goal
            if balls[i] == 0 or balls[i]  == 3 or balls[i] == 6:
                case_dist += 0
                man_dist += 0
            #4.push other snowball to the goal
            else:
                case_dist += math.sqrt((math.pow((i[0] - state.destination[0]),2)) + math.pow((i[1] - state.destination[1]),2))
                #case_dist += math.sqrt((math.pow((i[0] - state.robot[0]),2)) + math.pow((i[1] - state.robot[1]),2))
                man_dist += abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1])
                
        #5.balls are seperate and no relation to goal
        if (balls[i] == 0 and i != state.destination) or balls[i]  == 1 or balls[i] == 2 :
            case_dist += math.sqrt((math.pow((i[0] - state.destination[0]),2)) + math.pow((i[1] - state.destination[1]),2))
            #case_dist += math.sqrt((math.pow((i[0] - state.robot[0]),2)) + math.pow((i[1] - state.robot[1]),2))
            
            man_dist += abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1])
        #6.2 balls stack
        if (balls[i] == 3 and i != state.destination) or (balls[i] == 4 and i != state.destination) or (balls[i] == 5 and i != state.destination):
            case_dist += math.sqrt((math.pow((i[0] - state.destination[0]),2)) + math.pow((i[1] - state.destination[1]),2))
            #case_dist += math.sqrt((math.pow((i[0] - state.robot[0]),2)) + math.pow((i[1] - state.robot[1]),2))
            case_dist = 2*case_dist
            
            man_dist += abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1])
            man_dist = 2*man_dist
        #7.3 balls stack
        if (balls[i] == 6 and i != state.destination):
            case_dist += math.sqrt((math.pow((i[0] - state.destination[0]),2)) + math.pow((i[1] - state.destination[1]),2))
            #case_dist += math.sqrt((math.pow((i[0] - state.robot[0]),2)) + math.pow((i[1] - state.robot[1]),2))
            case_dist = 3*case_dist
            
            man_dist += abs(i[0] - state.destination[0]) + abs(i[1] - state.destination[1])
            man_dist = 3*man_dist
            
        optimal_dist = min(man_dist, case_dist)
        '''
        r_dist.append(abs(i[0] - state.robot[0]) + abs(i[1] - state.robot[1]))
    
    optimal_dist = min(r_dist) + man_dist
    return optimal_dist
    


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    fval = 0
    fval = sN.gval + (weight * sN.hval)
    return fval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
 
 
 #time
  s_time = os.times()[0]
  e_time = 0
  elapsed = 0
      
  #searcher
  f_function = (lambda sN : fval_function(sN, weight))
  h_function = (lambda state :  heur_alternate(state))
  searcher = SearchEngine('custom', 'full')
  searcher.init_search(initial_state, snowman_goal_state,h_function ,f_function)
  
  result = False
  cost_bound = (float("inf"), float("inf"), float("inf"))
  goal_result = searcher.search(timebound)
    
  while elapsed < timebound-2:
    if goal_result == False:
        return result
    
    e_time = os.times()[0]
    elapsed = e_time - s_time
      
    
    if goal_result:
        if goal_result.gval <= cost_bound[0]:
            result = goal_result
            cost_bound = (result.gval, result.gval, result.gval)
        
    goal_result = searcher.search(timebound - elapsed, cost_bound)
    
  return result



def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  
  #time
  s_time = os.times()[0]
  e_time = 0
  elapsed = 0
    
  #searcher
  searcher = SearchEngine('best_first', 'full')
  searcher.init_search(initial_state, snowman_goal_state, heur_fn)
  
  result = False
  
  cost_bound = (float("inf"), float("inf"), float("inf"))
  goal_result = searcher.search(timebound)
    
  while elapsed < timebound-2:
    if goal_result == False:
        return result
    
    e_time = os.times()[0]
    elapsed = e_time - s_time
    
    if goal_result:
        if goal_result.gval <= cost_bound[0]:
            result = goal_result
            cost_bound = (result.gval, result.gval, result.gval)
        
    goal_result = searcher.search(timebound - elapsed, cost_bound)
   
  return result

