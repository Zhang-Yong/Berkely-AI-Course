# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        print "action taken:", legalMoves[chosenIndex]
        print ""
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print "successorGameState", successorGameState
#         print "newPos", newPos
#         print "newFood", newFood
#         print "new Ghost position", successorGameState.getGhostPositions()
#        print "newScaredTimes", newScaredTimes
#         print "action & score", action, successorGameState.getScore()
        #Idea:3 factors to decide Agent's action, 1) newPos food info 2) newPos distance to food 3) newPos distance to Ghost
        # distance to food should have highest weight, live alive is most important !
         
        #score = (pacman2Ghost position) / (pacman postion to nearlist food distance).  
        #pacman2Ghost position: for several ghots distance = (min value)*5 + average value
        #while newscareTimes > 0, use constant to replace (pacman2Ghost position) , this factor is ignored for all actions
        #eat power pollet, newScaredTimes set to [40,40], -for each setp pacman move, -1.
        #Foods = successorGameState.getFood().asList()
        if action != "Stop":
            current_Food = currentGameState.getFood().asList()
            GhostPosition = successorGameState.getGhostPositions()
            Pac2Ghost = min(abs(newPos[0]-GP[0]) + abs(newPos[1]-GP[1]) for GP in GhostPosition)
            if len(newFood.asList()) > 0:
                Pac2Food = min(abs(newPos[0]-Fd[0]) +abs(newPos[1]-Fd[1]) for Fd in newFood.asList())
            else:  # No food to eat :)
                # nothing to eat, set it to a constant value and this number need to be small or last food will not eat
                Pac2Food = 1.0   
                
            # if there's power pollet, eat any way, set power_pollet to 100, unless Pac2Ghost is 0, this has no effect
            if newScaredTimes[0] > 0:
                Pac2Ghost = 1.0  # eat pollet, ignore Pac2Ghost distance, set a constant value here  
                power_factor = 100  
            else:   
                power_factor = 1.0
            # newPos has food, *10, else *1 
            if  newPos in   current_Food:
                food_factor = 10
            else:
                food_factor = 1.0
            
            #ghost close to pacman, enlarge pac2ghots,stay far way 
            if Pac2Ghost <= 3 and newScaredTimes[0] == 0 :
                Pac2Ghost = 20*Pac2Ghost
#             else:
#                 if Pac2Ghost <= 6 and newScaredTimes[0] == 0 :
#                     Pac2Ghost = 1*Pac2Ghost
#                 else:
#                     if Pac2Ghost > 6 and newScaredTimes[0] == 0 :
#                         Pac2Ghost = 1.0  # far away from ghost, ignore Pac2Ghost distance
#                 
            Score = power_factor*food_factor*Pac2Ghost / Pac2Food
        #print "pac2Ghost distance", Pac2Ghost
        else:   # action Stop case
            Score = 0
            
        #print "power_factor,food_factor,pac2Ghost, Pac2Food:", power_factor,food_factor, Pac2Ghost, Pac2Food
        print "Score, action:", Score, action
        return Score
        
        
        
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #Idea:   for depth, got pacman max value, ghost min value, and keep related action list, when loop
        #finished, return action list
        legalMoves = []
        successors = []
        self.visited_states_list = []
        current_state = gameState
        gameState_action_list = {}
        gameState_score_list = {}
        gameState_depth_list = {}
        gameState_agentIndex_list = {}
        gameState_successor_list = {}
        gameState_parent_node = {}
        #number of Agents
        agent_counter = current_state.getNumAgents()
        print 'agent_counter:', agent_counter
        print "self.depth", self.depth 
        #Generate a stack dict Grid to keep gamestate for every layer, and pop after each layer finish loop
        max_state_stack = util.Stack()
        min_state_stack = util.Stack()
        #similar as DFS, run through all state nodes, when all state in state stack has visited, set it to True        
        visit_all_state = False 
        Get_Top_Layer_Score = False
        self.init_gameState = gameState
        gameState_agentIndex_list[self.init_gameState] = 0
        #ghost_state_queue = util.Queue()
        init_depth = 1  # depth must start from 1
        min_agentIndex = 1
        max_agentIndex = 0
        current_agentIndex = 0
        #agentIndex = 0
        #*************** Begin of n depth iteration block ***********************
        #Idea, follow DFS algirothm, all Max,Min move push into stack, after loop, reach Terminal layer, evaluate score 
        while visit_all_state == False:
            for depth in range (init_depth, self.depth + 1   ):
                #********* Max move first *********#
                if current_agentIndex == 0:
                    legalMoves = gameState.getLegalActions(0)
                    if len(legalMoves) != 0:
                        for action in legalMoves:
                            successor_state = gameState.generateSuccessor(0, action)
                            max_state_stack.push(successor_state)
                            gameState_agentIndex_list[successor_state] =  1     
                            gameState_depth_list[successor_state] =  depth
                            #list use to compute recursively for score
                            gameState_parent_node[successor_state] = gameState
                            successors += [successor_state]
                            gameState_action_list[successor_state] = action
                            #print "Max state's successor Min push into stack, state, action :", successor_state, action
                            #print "init state", self.init_gameState
                        gameState_successor_list[gameState] =   successors
                        successors = []  
                        # call gamestate pop to update gameState
                        if  not max_state_stack.isEmpty(): 
                            gameState = max_state_stack.pop()
                            # Pop out gameState is successor, so need to Reset AgentIndex here
                            #agentIndex =  gameState_agentIndex_list[gameState]
                            current_agentIndex = 1
                            init_depth = gameState_depth_list[gameState]
                            print ""
                            print "Max state pop out stack, state, depth, agentIndex:", gameState,depth, current_agentIndex
                    else: # legalMove == 0
                        print "No legal move, terminal state, call getScore"
                        gameState_score_list[gameState] = self.evaluationFunction(gameState )
                        #print "Max state has no legal move, depth, current_agentIndex:" , gameState, depth,current_agentIndex
                        
                    #current_agentIndex = agentIndex + 1
                #*****Now all Mins Move  *******# 
                #------------------------------------------------------------------ Max, Min layer -------------------------------------#           
                #last depth, last Min will be excluded, do not need to generate successor
                if current_agentIndex > 0 :
                    if not (depth == self.depth and current_agentIndex == agent_counter -1):
                        for  index in range (current_agentIndex, agent_counter):
                            current_agentIndex = index
                            #print " this is Min move loop: ",current_agentIndex
                            legalMoves = gameState.getLegalActions(current_agentIndex)
                            if len(legalMoves) != 0:
                                for action in legalMoves:
                                    successor_state = gameState.generateSuccessor(current_agentIndex, action)
                                    min_state_stack.push(successor_state)
                                    #print "Min state push into stack, state, depth, agentIndex:", successor_state,depth, agentIndex
                                    #successor state ! Need Adjust agentIndex for next gameState pop 
                                    if  current_agentIndex <  agent_counter - 1:  # Min agent, not last one
                                        gameState_agentIndex_list[successor_state] = current_agentIndex + 1 # successor is 1
                                        gameState_depth_list[successor_state] = depth
                                    if  current_agentIndex ==  agent_counter - 1:   # last Min agent index, then turn to Max agent
                                        gameState_agentIndex_list[successor_state] = 0
                                        gameState_depth_list[successor_state] =  depth + 1
                                    
                                    gameState_parent_node[successor_state] = gameState    
                                    successors += [successor_state]
                                    gameState_action_list[successor_state] = action
                                gameState_successor_list[gameState] =   successors
                                successors = []
                            else:
                                print "No legal move, terminal state, call getScore"
                                gameState_score_list[gameState] = self.evaluationFunction(gameState )
                                #print "Min state has no legal move, depth, agentIndex:" , gameState, depth,current_agentIndex
                                   
                            # Update gameState for next layer Min move 
                            # last layer last Min do not pop, get score directly
                            if not (depth == self.depth and current_agentIndex == agent_counter -1):
                                if  not min_state_stack.isEmpty(): 
                                    gameState = min_state_stack.pop()
                                    # Pop out gameState is successor, so need to Reset AgentIndex here
                                    current_agentIndex =  gameState_agentIndex_list[gameState]
                                    #init_depth = gameState_depth_list[gameState]
                                    #print "Min state pop out stack, state, depth, agentIndex after:", gameState,gameState_depth_list[gameState], gameState_agentIndex_list[gameState]
                                    #*****************end of all Mins move *****************#
            #Reach Terminal layer, get Score, else pop next gamestate 
            print "depth, current_agentIndex before if", depth, current_agentIndex    
            if  depth == self.depth  and  current_agentIndex ==  agent_counter - 1:  
                print "depth, current_agentIndex before score", depth, current_agentIndex
                gameState_score_list[gameState] = self.evaluationFunction(gameState )
            #print ""
            #print "state Scored ! state,depth,agentIndex, socre:", gameState,depth, current_agentIndex,  gameState_score_list[gameState]
            #****************end of  1 iteration DFS tree search ********************#
            #next node branch DFS search 
            if  min_state_stack.isEmpty() and max_state_stack.isEmpty():
                visit_all_state = True
            else: # pop out next game state, determin its depth and agentIndex info
                if  not min_state_stack.isEmpty(): 
                    gameState = min_state_stack.pop()
                else:
                    if  not max_state_stack.isEmpty():
                        gameState = max_state_stack.pop()
                    # Pop out gameState is successor, so need to Reset AgentIndex here
                current_agentIndex =  gameState_agentIndex_list[gameState]
                init_depth = gameState_depth_list[gameState]
                #print "New branch state pop out stack, state, depth, agentIndex:", gameState,depth, current_agentIndex
            #end of all ghots response, generate all ghost gamestates
        #**************End of n depth iteration, pacman move, all ghosts response**********************#  
         
        print "Terminal layer Score", gameState_score_list.values()  
#         print "Terminal layer list", gameState_score_list.keys()  
#         print " paranent node list1",gameState_parent_node.keys()
#         print " paranent node list2",gameState_parent_node.keys()
#         print "agendIndex list",gameState_agentIndex_list.keys()
#         print " all successor", gameState_successor_list.values()
#         print " paranent node list",gameState_parent_node.values()
#         print "agendIndex list",gameState_agentIndex_list.keys()
#         print "agendIndex values",gameState_agentIndex_list.values()
#         for state in  gameState_successor_list.values():
#             print "successor state ", state
                
        #Return final action of init gameState
        def return_action(self):
            #print "init gameState_successor_list",gameState_successor_list[self.init_gameState]
            for state in gameState_successor_list[self.init_gameState]:
                if  gameState_score_list[self.init_gameState] == gameState_score_list[state]:
                    #print "init state value", gameState_score_list[self.init_gameState]
                    #print "successor state value",gameState_score_list[state]
                    return gameState_action_list[state]
         
        #Max layer, get  Max score of  child states for its parent state 
        def update_parent_layer_Score(self):
            #maxScore = float("-inf ") 
            #minScore = float("inf ")
            maxScore = {}
            minScore = {}  
            #visited_states_list = []
            #max_last_parent = self.init_gameState
            max_last_parent = 0
            min_last_parent = 0
            parent_state_list = []
            #after for loop, all parent layers should have been updated
            for state in gameState_score_list.keys():  # first time run, only keep Terminal layer in the list
                if state not in self.visited_states_list:
                    print "state Score:", gameState_score_list[state]
                    #assign one terminal state value to its parent node  
                    current_parent_state = gameState_parent_node[state]  
                    
                    #****************check for terminal layer tree structure block **********#
                    #Update for test case fail of terminal layer has a tree structure, parent state need to check value before update
                    #by child state
                    if gameState_score_list.has_key(current_parent_state):
                        #Max layer, get max value
                        if gameState_agentIndex_list[current_parent_state] == 0:
                            if gameState_score_list[current_parent_state] < gameState_score_list[state]:
                                gameState_score_list[current_parent_state] = gameState_score_list[state]
                        else:  # Min layer, get Min value, parent state score > child score, update parent state value
                            if gameState_score_list[current_parent_state] > gameState_score_list[state]:
                                gameState_score_list[current_parent_state] = gameState_score_list[state]
                    else:  # Normal case, terminal layer is a single layer
                        gameState_score_list[current_parent_state] = gameState_score_list[state]
                    #######***********End of Block *************************###################
                                 
                    #**************Parent layer is Max layer, get Max value ******************#
                    #print "Index value:", gameState_agentIndex_list[current_parent_state]
                    if gameState_agentIndex_list[current_parent_state] == 0:
                        #reset maxSocre value for different parent/child states
                        if current_parent_state not in parent_state_list:
                            maxScore[current_parent_state] = float("-inf ") 
                            #print ' not equal'
                            #print "max last  parent", max_last_parent
                            #print "current parent state", current_parent_state
                          
                        if  gameState_score_list[current_parent_state] >  maxScore[current_parent_state]:
                            maxScore[current_parent_state] = gameState_score_list[current_parent_state]
                            # Find out seletcted states
                            if gameState_score_list.has_key(self.init_gameState):
                                self.selected_state = state
                        else:
                            gameState_score_list[current_parent_state] = maxScore[current_parent_state]
                    #****************Min layer update *********************************#        
                    else: #Parent layer is Min layer, get min value
                        #reset maxSocre value for different parent/child states, max/min score should seperate for diff gamestate
                        if  current_parent_state not in parent_state_list:
                            minScore[current_parent_state] = float("inf ")  
                        #paranet state value assigned as child current state value in the beginning 
                        #update minScore if less than minScore, otherwise, use minSocre to update parent node value
                        if  gameState_score_list[current_parent_state] <  minScore[current_parent_state]:
                            minScore[current_parent_state] = gameState_score_list[current_parent_state]
                        else:
                            gameState_score_list[current_parent_state] = minScore[current_parent_state]
                        
                        #print "minScore,parent_state", current_parent_state, minScore[current_parent_state]
                        
                    parent_state_list += [current_parent_state]
                    
                self.visited_states_list += [state]
                     
                
            print "Max  layer Score:",   maxScore.values()
            #print out max successor group 
#             for state in maxScore.keys():
#                 print ""
#                 for successor in gameState_successor_list[state]:
#                     print "Max layer successor_score_list",gameState_score_list[successor]
            
            #Print out min successor group        
            print "Min  layer Score:",   minScore.values()            
#             for state in minScore.keys():
#                 print ""
#                 for successor in gameState_successor_list[state]:
#                     print "Min layer successor_score_list",gameState_score_list[successor]
                    
            #print 'layer updated,maxScore, minScore ',  maxScore,  minScore   
            #print "update score:",gameState_score_list.values()
            #return gameState_score_list[parent_state]
        
        
        #**************Begin loop of compute recurisively ***********************#
        #While loop to compute recursively to get score of each layer
        
        while Get_Top_Layer_Score == False:
            update_parent_layer_Score(self)
            if  gameState_score_list.has_key(self.init_gameState):
                Get_Top_Layer_Score = True
                print "action find  !", gameState_score_list[self.init_gameState]
                print 'all score ',gameState_score_list.values()
                #action = return_action(self)
                action = gameState_action_list[self.selected_state]
                return action
        #return_action(self)
    
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = []
        successors = []
        self.visited_states_list = []
        gameState_action_list = {}
        gameState_score_list = {}
        gameState_agentIndex_list = {}
        gameState_successor_list = {}
        init_gameState = gameState
        gameState_agentIndex_list[init_gameState] = 0
        #number of Agents
        agent_counter = init_gameState.getNumAgents()
        print 'agent_counter:', agent_counter
        print "self.depth", self.depth
        # fix depth bug, need +1.  
        depth = self.depth +1
        agentIndex = 0
        alpha = float("-inf")
        belta = float("inf")
        
        #*************** Begin of n depth iteration block ***********************
        # General alpha belta prunning algirothm, need to adjust depth and agent index value  
        # according to multi ghost case !
        #The follow func will update all state values
        def  alphabeta(gameState,depth, alpha, belta, agentIndex):
            # Teriminal state, return score
            if (depth == 0  and agentIndex == agent_counter -1) or is_Terminal_state(gameState,agentIndex):
                gameState_score_list[gameState] = self.evaluationFunction(gameState )
                print "terminal gameState Score",gameState_score_list[gameState]
                return gameState_score_list[gameState]
            
            #if maximizingPlayer
            if agentIndex == 0: 
                v = float("-inf")
                successors = []
                legalMoves = gameState.getLegalActions(agentIndex)
                for action in legalMoves:
                    child = gameState.generateSuccessor(agentIndex, action)
                    v = max(v, alphabeta(child, depth - 1, alpha, belta, agentIndex + 1))
                    alpha = max(alpha, v)
                    #print "alpha, belta, in Max:", alpha, belta
                    #print "depth, agentIndex in Max", depth, agentIndex
                    #keep info in dict
                    successors += [child]
                    gameState_action_list[child] = action
                    gameState_successor_list[gameState] =   successors
                    
                    if  v >= belta:
                        #print ""
                        #print "break here in Max"
                        gameState_score_list[gameState] = v
                        return v #(* Belta cut-off *)
                    
                gameState_score_list[gameState] = v 
                return v
            else:   # Min ghost player
                v = float("inf")
                successors = []
                legalMoves = gameState.getLegalActions(agentIndex)
                for action in legalMoves:
                    child = gameState.generateSuccessor(agentIndex, action)
                    #check agentIndex for multi ghost case, multi-ghost, +1, 0 for 1 ghost
                    if agentIndex < agent_counter -1:
                        v = min(v, alphabeta(child, depth , alpha, belta, agentIndex + 1))
                    else: # fix bug of depth, reach last min agent, depth -1,  agent set to 0
                        v = min(v, alphabeta(child, depth -1 , alpha, belta, 0))
                        
                    belta = min(belta, v)
                    #print "alpha, belta in Min:", alpha, belta
                    #print "depth,agentIndex in Min", depth, agentIndex
                    #keep info in dict
                    successors += [child]
                    gameState_action_list[child] = action
                    gameState_successor_list[gameState] =   successors

                    if v <= alpha:
                        #print ""
                        #print "break here in Min"
                        gameState_score_list[gameState] = v
                        return v  #(* Alpha cut-off *)
                    
                gameState_score_list[gameState] = v
                return v

                        
        def is_Terminal_state(gameState,agentIndex):
            legalMoves = gameState.getLegalActions(agentIndex)
            if len(legalMoves) == 0:
                print " Terminal state"
                return True
            else:
                return False
                
        def Get_action():
            if  gameState_score_list.has_key(init_gameState):
                successors = gameState_successor_list[init_gameState]
                for  item in successors:
                    if gameState_score_list[ init_gameState] == gameState_score_list[item]:
                        target_action = gameState_action_list[item]
                        return target_action     
          
        #Main program here  
        alphabeta(gameState,depth, alpha, belta, agentIndex)
        #print "all layer score:",gameState_score_list.values()
        action = Get_action()  
        return action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves = []
        successors = []
        self.visited_states_list = []
        gameState_action_list = {}
        gameState_score_list = {}
        gameState_agentIndex_list = {}
        gameState_successor_list = {}
        
        #similar as DFS, run through all state nodes, when all state in state stack has visited, set it to True        
        init_gameState = gameState
        gameState_agentIndex_list[init_gameState] = 0
        #number of Agents
        agent_counter = init_gameState.getNumAgents()
        print 'agent_counter:', agent_counter
        print "self.depth", self.depth
        # fix depth bug, need +1.  
        depth = self.depth +1
        #ghost_state_queue = util.Queue()
        agentIndex = 0
        alpha = float("-inf")
        belta = float("inf")
        
        #*************** ExpectiMax ***********************
        # General alpha belta prunning algirothm, need to adjust depth and agent index value  
        # according to multi ghost case !
        #The follow func will update all state values
        # Difference of ExpectiMax with MiniMax Pruning: No node trimming in Min, Max still use Max value, Min use probability 
        #average instead of Min value
        def  ExpectiMax(gameState,depth, alpha, belta, agentIndex):
            # Teriminal state, return score
            if (depth == 0  and agentIndex == agent_counter -1) or is_Terminal_state(gameState,agentIndex):
                gameState_score_list[gameState] = self.evaluationFunction(gameState )
                #print "terminal gameState Score",gameState_score_list[gameState]
                return gameState_score_list[gameState]
            
            #if maximizingPlayer
            if agentIndex == 0: 
                v = float("-inf")
                successors = []
                legalMoves = gameState.getLegalActions(agentIndex)
                for action in legalMoves:
                    child = gameState.generateSuccessor(agentIndex, action)
                    v = max(v, ExpectiMax(child, depth - 1, alpha, belta, agentIndex + 1))
                    alpha = max(alpha, v)
                    #print "alpha, belta, in Max:", alpha, belta
                    #print "depth, agentIndex in Max", depth, agentIndex
                    #keep info in dict
                    successors += [child]
                    gameState_action_list[child] = action
                    gameState_successor_list[gameState] =   successors
                    
                    if  v >= belta:
                        #print ""
                        #print "break here in Max"
                        gameState_score_list[gameState] = v
                        return v #(* Belta cut-off *)
                    
                gameState_score_list[gameState] = v 
                return v
            else:   # Min ghost player
                #v = float("inf")
                v = 0.0
                successors = []
                legalMoves = gameState.getLegalActions(agentIndex)
                probability =  1.0/len(legalMoves)
                for action in legalMoves:
                    child = gameState.generateSuccessor(agentIndex, action)
                    #check agentIndex for multi ghost case, multi-ghost, +1, 0 for 1 ghost
                    if agentIndex < agent_counter -1:
                        #v = min(v, ExpectiMax(child, depth , alpha, belta, agentIndex + 1))
                        v +=  probability*ExpectiMax(child, depth , alpha, belta, agentIndex + 1)
                    else: # fix bug of depth, reach last min agent, depth -1,  agent set to 0
                        #v = min(v, ExpectiMax(child, depth -1 , alpha, belta, 0))
                        v +=  probability*ExpectiMax(child, depth , alpha, belta, 0)
                    belta = min(belta, v)
                    #print "alpha, belta in Min:", alpha, belta
                    #print "depth,agentIndex in Min", depth, agentIndex
                    #keep info in dict
                    successors += [child]
                    gameState_action_list[child] = action
                    gameState_successor_list[gameState] =   successors

#                     if v <= alpha:
#                         print ""
#                         print "break here in Min"
#                         gameState_score_list[gameState] = v
#                         return v  #(* Alpha cut-off *)
                    
                gameState_score_list[gameState] = v
                return v

                        
        def is_Terminal_state(gameState,agentIndex):
            legalMoves = gameState.getLegalActions(agentIndex)
            if len(legalMoves) == 0:
                print " Terminal state"
                return True
            else:
                return False
            
        def Get_action():
            if  gameState_score_list.has_key(init_gameState):
                successors = gameState_successor_list[init_gameState]
                for  item in successors:
                    if gameState_score_list[ init_gameState] == gameState_score_list[item]:
                        target_action = gameState_action_list[item]
                        return target_action     
                    
        #Main program here  
        ExpectiMax(gameState,depth, alpha, belta, agentIndex)
        print "all layer score:",gameState_score_list.values()
        action = Get_action()  
        return action
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
     Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Athlon, 2/2, 2016
      feathures to evaluate gameState: 
      Eat food,  distance to ghost, pacman distance to food,distance to power pollet, eat power pollet. 
    """
    "*** YOUR CODE HERE ***"
    
    #Idea:3 factors to decide Agent's action, 1) newPos food info 2) newPos distance to food 3) newPos distance to Ghost
        # distance to food should have highest weight, live alive is most important !
         
        #score = (pacman2Ghost position) / (pacman postion to nearlist food distance).  
        #pacman2Ghost position: for several ghots distance = (min value)*5 + average value
        #while newscareTimes > 0, use constant to replace (pacman2Ghost position) , this factor is ignored for all actions
        #eat power pollet, newScaredTimes set to [40,40], -for each setp pacman move, -1.
        #Foods = successorGameState.getFood().asList()
        
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
#     newPos = successorGameState.getPacmanPosition()
#     newFood = successorGameState.getFood()
#     newGhostStates = successorGameState.getGhostStates()
#     newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    import searchAgents
    Pacman_Position =    currentGameState.getPacmanPosition()
    #print "Pacman position", Pacman_Position
    Food = currentGameState.getFood().asList()
    Ghost_Position = currentGameState.getGhostPositions()
    #print " Ghost postion", Ghost_Position
    capsules_Position = currentGameState.getCapsules()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    #define weight parametes here
    Weight_Pac2Ghost = 0.0
    Weight_Pac2Food = 20.0
    Weight_Pac2Cap =  5
    Weight_eat_food = 30
    #get the distance to closet ghost, ignore the others
    #print "ghost postion,",Ghost_Position
    
    #convert float number position to integer position
    def convert_to_integer(position):
        x,y = position
        x = int(x)
        y = int(y)
        return (x,y)
    
    distance = float ("inf")
    for GP in Ghost_Position:
        #print "GP before convert", GP
        #Turn float to int number
        GP_new = convert_to_integer(GP)
        #print " GP after convert", GP_new
        Pac2Ghost = searchAgents.mazeDistance(Pacman_Position, GP_new, currentGameState)    
        Pac2Ghost = min(distance,Pac2Ghost)
        #Pac2Ghost = Pac2Ghost*Weight_Pac2Ghost
        #Pac2Ghost = min(abs(newPos[0]-GP[0]) + abs(newPos[1]-GP[1]) for GP in GhostPosition)
    #get pacman distance to power pollet
    if len(capsules_Position) > 0:
        Pac2Cap = min(searchAgents.mazeDistance(Pacman_Position, cap, currentGameState) for cap in capsules_Position)    
    else:  # factor will be multiply, set to 1.0 to ignore this factor
        Pac2Cap = 1.0
    
    #Get pacman distance to closet food    
    if len(Food) > 0:
        Pac2Food = min(searchAgents.mazeDistance(Pacman_Position, Fd, currentGameState) for Fd in Food)
        #a lot of case it will be 1, same value as no food, so add weight for food distance 
        #Pac2Food = Weight_Pac2Food/Pac2Food
    else:  # No food to eat :)
        # nothing to eat, set it to a constant value and this number need to be small or last food will not eat
        Pac2Food = 0.0   
        
    # if eat power pollet, ingore pacman distace to Ghost
    if ScaredTimes[0] > 0:
        Pac2Ghost = 0.0  # eat pollet, ignore Pac2Ghost distance, set a constant value here
          
    # if Pacman position has food, *10, else *1
    if currentGameState.data._foodEaten == Pacman_Position:
        print " current pos has food", Pacman_Position
        eat_food = 1.0
    else:
        eat_food = 0.0
    
    Score = Weight_eat_food*eat_food 
    #Score =  Weight_eat_food*eat_food + Weight_Pac2Ghost*Pac2Ghost +  Weight_Pac2Food/Pac2Food +  Weight_Pac2Food/Pac2Cap
    print "score:", Score
    return Score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

