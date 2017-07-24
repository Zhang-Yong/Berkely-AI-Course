# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from hgext.inotify.server import start


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Algorithm: unvisited state 1st priopirty, if no way to go, choose ( old way) small index number in state list
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    #print " item 0", problem.getSuccessors(problem.getStartState())[0][0]
    # init list here
   
    current_actions = []
    actions_list = []
    running = True
    current_state_successors = []
    
    # keep all successor state into LIFO 
    state_stack = util.Stack()
    visited_states = []
    action_stack = util.Stack()
            
    # incase start state is goal state, return action none
    current_state = problem.getStartState()
    # add start state into visited states list
    visited_states.append( current_state)
    

    if problem.isGoalState(current_state):
          print " start status is Goal status ! Action none "
          return None
    else:
      while running:
        # Extract successor and direction:format: [((x0,y0),'direction0', cost0),(x1,y1),'direction1', cost1)] 
        for item in problem.getSuccessors(current_state):
          if item[0] not in visited_states:
            state_stack.push(item[0])
            #print "item[0]", item[0]
            #record all actions in FIFO
            action_stack.push(item[1])
            # keep current state successors to check if state jump to last node, as pacman can not     jump, only keep un-visited state, so when it is empty, means no way to go
            current_state_successors.append(item[0])
          #print "state stack list", state_stack.list 
        #No way to go, choose old way first, which is min index state
        if len(current_state_successors) == 0:
          first_state = problem.getSuccessors(current_state)[0][0]
          min_state_index =  visited_states.index(first_state) 
          for item in problem.getSuccessors(current_state): # find out min index ( old way) way
            if visited_states.index(item[0]) <= min_state_index:            
              min_state_index = visited_states.index(item[0])
              action_stack.push(item[1]) 
              
          # assign old way to successor state 
          successor_state = visited_states[min_state_index]
          #print " action stack list2 ",action_stack.list 
          current_action = action_stack.pop()
            

        # there's un-visted state, stack keep un-visited nodes
        else: 
          successor_state = state_stack.pop()
          current_action = action_stack.pop()

        
        #print "successor state", successor_state
        #print "current action ", current_action

        
        #recode action history here
        actions_list.append(current_action)
        # keep update visited states list
        if successor_state in visited_states:
          # Del same visited state before append
          visited_states.remove(successor_state)    
        visited_states.append(successor_state) 
        
        #print " actions list ", actions_list
        #print " visted states ", visited_states
                          
        
        # check if current state is goal       
        if problem.isGoalState(successor_state):
          running = False
          #print " Goal founded, state is: ", successor_state
          #print " Action sequence is: ", actions_list
          return actions_list
          #break

        else:
          #current state is not goal, expand trees to search
          # Update current state
          current_state = successor_state

          #clear current_state successor for next state
          current_state_successors = []  
        

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Algorithm: loop for each successor, if Goal --> generate action list (from Goal to startpoint, check
    #last node successor and related action ) 
    #else --> push unvisited state 
    # into FIFO queue, high level node push into FIFO first, then low level, same level state 
    # will continously push into FIFO and check goal

    # init list here
    actions_list = []
    running = True
    #state_index = []
    # keep all successor state into FIFO 
    state_queue = util.Queue()
    visited_states_actions = {}
    visited_states_list = []
                
    # incase start state is goal state, return action none
    current_state = problem.getStartState()
    start_state = problem.getStartState()
    # add start state into visited states list
    #visited_states.append( current_state)
    #visited_states_list.append( start_state)
    #**!!!! Use empty list for first empty action !!!!
    visited_states_actions[start_state] = []
    
    #print "start state", problem.getStartState()
     
    if problem.isGoalState(current_state):
        print " start status is Goal status ! Action none "
        #return None
        #Fix bug in Mazedistance to calculate distance of any two points, at the case first state is Goal, return None
        #will generate error
        return visited_states_actions[start_state]
    else:
        while running:
            # all successor states put into queue with priority 
            #start state and corner state case,  for  start state will be appended below
            #corner state case, visited state list clear to 0, explore from corner node
            #empty command to run getSuccessors pass info to getStartState() 
            
            #*****begin of corner case block ********# All code use current_state instead of successor state
            problem.getSuccessors(current_state)  # run this func so that all flags are updated
            if current_state == problem.getStartState():
                if current_state == start_state:
                    visited_states_list.append( start_state)
                else:  # corner case
                    print " corner case:", current_state
                    #corner case, need to clear all info from start state
                    # clear visited sates, clear action dictionary, resotre corner state action
                    visited_states_list = []
                    current_state_action =  visited_states_actions[current_state]
                    #print " state action results before clear",visited_states_actions
                    visited_states_actions.clear()
                    visited_states_actions[current_state] = current_state_action
                    #print  "corner state action", current_state,visited_states_actions[current_state] 
                    # init state quote to clear push state
                    # Remember to append current state after clear !
                    visited_states_list.append(current_state)
                    
                    while not state_queue.isEmpty():
                        state_queue.pop()
            #******end of corner case block ***********#  
            for item in problem.getSuccessors(current_state):
                #print "current state: ", current_state
                if item[0] not in visited_states_list:
                    #Non start state or corner state, assign paranent node actions list first here
                    #if current_state != problem.getStartState():
                    #if current_state != start_state:
                        #!!! assign address only in Python, action_list update will update visited_states !!!
                        #actions_list = visited_states[current_state]
                    #import copy
                    #actions_list = copy.deepcopy(visited_states_actions[current_state])
                    #!!! Do not use "append" , this will add addtional []. 
                    # !!! use list = list + visited_states_action[] or use copy.deepcopy function
                    
                    #***!!! need to comment code below, start state will be accessed multi-times,
                    #***!!! next time it will make action list data error
                    #if current_state != start_state:    # ignore start state 
                    actions_list = actions_list + visited_states_actions[current_state]
                        #print "action list before append", visited_states_actions[current_state]
                    #child node action list here
                    actions_list.append(item[1]) 
                    #print "item[1]" , item[1]
                    #get state cost, getCostofActions func return cost from start_state
                    #priority = problem.getCostOfActions(actions_list)
                    #push all successor priority into queue
                    state_queue.push(item[0])
                    #save in a dict, which contain state and action list from startpoint
                    visited_states_actions[item[0]] =  actions_list
                    #change to item[0]
                    #visited_states_list.append(current_state)
                    visited_states_list.append(item[0])
                    #print " visited states actions", visited_states_actions
                    #clear action list for next successors
                    actions_list = []
                    #print "action list: should empty", actions_list
                    
            #poped result is FIFO  
            if not state_queue.isEmpty():
                successor_state = state_queue.pop()
                #print " pop successor state", successor_state
            #else:
                #print " state queue is empty, can not pop"
            #print " visited states, actions", visited_states_actions
            # check if current state is goal, generate action list       
            #if problem.isGoalState(successor_state):
            if problem.isGoalState(current_state):  #use current state instead of successor state
                running = False
                #print " Goal founded,state: ", current_state,visited_states_actions
                return visited_states_actions[current_state]
            else:
                current_state =  successor_state
             
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    """UFS Idea: loop do: Generate a dictionary with {state: actions} value for all states
       actions are lists recodered start from startpoint
       each state are push into priority queue with priority( cummulative cost from start )
       pop from queue will pop min value which is least cost value first.
       check goal, update current result with successor state

       BFS idea: same, only use FIFO queue. same level node expand first
       DFS idea: same, only use LIFO queue. nodes are put into queue, last level node expand first 
                 when no way to go
         """
    # init list here
    actions_list = []
    running = True
    #state_index = []
    # keep all successor state into LIFO 
    state_priority_queue = util.PriorityQueue()
    visited_states = {}
    # incase start state is goal state, return action none
    current_state = problem.getStartState()
    start_state = problem.getStartState()
    # add start state into visited states list
    visited_states[start_state] = None

    if problem.isGoalState(current_state):
        print " start status is Goal status ! Action none "
        return None
    else:
        while running:
            # all successor states put into queue with priority 
            for item in problem.getSuccessors(current_state):
                                           
                if item[0] not in visited_states:
                    #assign paranent node actions list first here
                    if current_state != start_state:
                        #!!! assign address onlu in Python
                        #actions_list = visited_states[current_state]
                        import copy
                        actions_list = copy.deepcopy(visited_states[current_state])
                    #child node action list here
                    actions_list.append(item[1]) 
                    #get state cost, getCostofActions func return cost from start_state
                    priority = problem.getCostOfActions(actions_list)
                    #push all successor priority into queue
                    state_priority_queue.push(item[0],priority)
                    #save in a dict, which contain state and action list from startpoint
                    visited_states[item[0]] =  actions_list
                        
                    #clear action list for next successors
                    actions_list = []
                    #print "action list: should empty", actions_list
            #poped result is min value of priority  
            successor_state = state_priority_queue.pop()
            # check if current state is goal, generate action list       
            if problem.isGoalState(successor_state):
                running = False
           
                return visited_states[successor_state]
            else:
                current_state =  successor_state
                    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # init list here
    actions_list = []
    running = True
    #state_index = []
    # keep all successor state into LIFO 
    state_priority_queue = util.PriorityQueue()
    visited_states_actions = {}
    visited_states_list = []
    # incase start state is goal state, return action none
    current_state = problem.getStartState()
    start_state = problem.getStartState()
    # add start state into visited states list
    visited_states_actions[start_state] = None
  

    if problem.isGoalState(current_state):
        print " start status is Goal status ! Action none "
        return None
    else:
        while running:
            #*****begin of corner case block ********# All code use current_state instead of successor state
            problem.getSuccessors(current_state)
            if current_state == problem.getStartState():
                if current_state == start_state:
                    visited_states_list.append( start_state)
                else:  # corner case
                    print " corner case:", current_state
                    #corner case, need to clear all info from start state
                    # clear visited sates, clear action dictionary, resotre corner state action
                    visited_states_list = []
                    current_state_action =  visited_states_actions[current_state]
                    print " state action results before clear",visited_states_actions
                    visited_states_actions.clear()
                    visited_states_actions[current_state] = current_state_action
                    print  "corner state action", current_state,visited_states_actions[current_state] 
                    
                    # Remember to append current state after clear !
                    visited_states_list.append(current_state)
                    
                    # init state quote to clear push state
                    while not state_priority_queue.isEmpty():
                        state_priority_queue.pop()
            #******end of corner case block ***********#  
            # all successor states put into queue with priority 
            for item in problem.getSuccessors(current_state):
                if item[0] not in visited_states_list:
                    #assign paranent node actions list first here
                    #if current_state != start_state:
                        #!!! assign address onlu in Python
                        #actions_list = visited_states[current_state]
                        #import copy
                        #actions_list = copy.deepcopy(visited_states[current_state])
                    #actions_list = actions_list + visited_states_actions[current_state]
                    if current_state != start_state:
                        #!!! assign address onlu in Python
                        #actions_list = visited_states[current_state]
                        import copy
                        actions_list = copy.deepcopy(visited_states_actions[current_state])
                    #child node action list here
                    actions_list.append(item[1]) 
                    #get state cost, getCostofActions func return cost from start_state
                    G = problem.getCostOfActions(actions_list)
                    #get nullHeuristic function
                    H = heuristic(item[0],problem)
                    #print " Heuristic result: ", H
                    #get F function
                    F = G + H  
                    #push all successor priority into queue
                    state_priority_queue.push(item[0],F)
                    #save in a dict, which contain state and action list from startpoint
                    visited_states_actions[item[0]] =  actions_list
                     
                    #!!! remember to add, visited_states_list.append(current_state)
                    visited_states_list.append(item[0])   
                    
                    #clear action list for next successors
                    actions_list = []
                    #print "action list: should empty", actions_list
            #poped result is min value of priority  
            successor_state = state_priority_queue.pop()
            # check if current state is goal, generate action list       
            if problem.isGoalState(successor_state):
                running = False
           
                return visited_states_actions[successor_state]
            else:
                current_state =  successor_state

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
