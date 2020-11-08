from world_state_data import WorldStateData

class WorldState:
    def __init__(self, prevState=None):
        """
        Generates a new state by copying information from its predecessor.
        """
        self.data = WorldStateData()
    
    def getLegalActions(self, agentIndex):
        """
        Returns the legal actions for the agent specified.
        """
        pass
    
    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        pass
