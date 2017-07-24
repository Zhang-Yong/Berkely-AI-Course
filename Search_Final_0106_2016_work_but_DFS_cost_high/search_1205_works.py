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

        
        print "successor state", successor_state
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
    state_index = []
    # keep all successor state into LIFO 
    state_queue = util.Queue()
    visited_states = []
                
    # incase start state is goal state, return action none
    current_state = problem.getStartState()
    start_state = problem.getStartState()
    # add start state into visited states list
    visited_states.append( current_state)
    
    print "start state", problem.getStartState()

    if problem.isGoalState(current_state):
      print " start status is Goal status ! Action none "
      return None
    else:
      while running:
        # Extract successor and direction:format: [((x0,y0),'direction0', cost0),(x1,y1),'direction1', cost1)] 
        for item in problem.getSuccessors(current_state):
          if item[0] not in visited_states:
            state_queue.push(item[0])
                    
        # BFS, check all un-visted states if it's goal 
        while state_queue.isEmpty() == False: 
          successor_state = state_queue.pop()
          #keep visited states
          visited_states.append(successor_state) 
                                       
          # check if current state is goal, generate action list       
          if problem.isGoalState(successor_state):
            running = False
        
            # Find Goal! Code below is for generate action lists here
            # Idea: 1) Record goal state 2) check if successor state in visited list
            # 3) select min index state (node level high) 4) repeat 2,3 until reach start point 5) generate list
            Goal = successor_state
            print " Find Goal ! ", Goal            
            current_node = Goal
            #Bottom--> Top way to find out Goal to startpoint path
            while  current_node != problem.getStartState():
              #Assign last level node to Goal
              #Assign min index state
              min_state_index=min(visited_states.index(item[0]) for item in problem.getSuccessors(current_node))
              last_node = visited_states[min_state_index]
              
              #find out related action to last level node
              for item in problem.getSuccessors(current_node):
                if item[0] == last_node:
                  current_action = item[1]
              
              # Generate action list here, REVERSE first, then reverse
              from game import Directions
              current_action = Directions.REVERSE[current_action]
              actions_list.append(current_action)

              #update current node to keep while loop running
              current_node = last_node
                       
            #after while loop, list is generated, reverse finally
            actions_list.reverse()     
            return actions_list
          
          else:
            #current state is not goal, push his un-visited successor into stack, need FIFO here
            # contiune check goal or not in while loop
            for item in problem.getSuccessors(successor_state):
              if item[0] not in visited_states:
                state_queue.push(item[0])
             
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
                    G = problem.getCostOfActions(actions_list)
                    #get nullHeuristic function
                    H = heuristic(item[0],problem)
                    print " Heuristic result: ", H
                    #get F function
                    F = G + H  
                    #push all successor priority into queue
                    state_priority_queue.push(item[0],F)
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


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
