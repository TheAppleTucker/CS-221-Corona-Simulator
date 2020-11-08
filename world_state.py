from world_state_data import WorldStateData

class WorldState:    
    def getLegalActions(self, agentIndex):
        """
        Returns the legal actions for the agent specified.
        """
        if self.isEnd():
            return []
        if agentIndex == 0:
            return GovtRules.getLegalActions(self)
        else:
            return COVIDRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isEnd(): raise Exception('Can\'t generate a successor of a terminal state.')
        
        # Copy current state
        state = GameState(self)

        if agentIndex == 0:
            GovtRules.applyAction(state, action)
        else:
            COVIDRules.applyAction(state, action, agentIndex)

        state.data.score += state.data._numInfected
        return state

    def isEnd(self):
        return self.data.isEnd

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################
    def __init__(self, prevState = None, maxLevel = 10):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState is not None: # Initial state
            self.data = GameStateData(prevState.data)
            self.maxLevel = prevState.maxLevel
        else:
            self.data = GameStateData()
            self.maxLevel = maxLevel

    def deepCopy(self):
        state = GameState( self )
        state.data = self.data.deepCopy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        if other is None: return False
        return self.data == other.data

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.data)

    def __str__(self):
        return str(self.data)


class GovtRules:
    class Actions:
        LOCKDOWN = 'Lockdown'
        REOPEN = 'Reopen'
        IDLE = 'Idle'
    """
    These functions govern how govt interacts with his environment under the classic rules.
    """
    def getLegalActions(state):
        """
        Returns a list of possible actions.
        """
        ngrids = len(state.data.grids)
        lockdowns = [(GovtRules.Actions.LOCKDOWN, i) for i in range(ngrids) \
                    if !state.data.grids[i].isLockdown and !state.data.grids[i].isInfected]
        reopen = [(GovtRules.Actions.REOPEN, i) for i in range(ngrids) \
                if state.data.grids[i].isLockdown and !state.data.grids[i].isInfected]
        return lockdowns + reopen + [(GovtRules.Actions.IDLE, -1)]
    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action):
        """
        Edits the state to reflect the results of the action.
        """
        legal = GovtRules.getLegalActions( state )
        if action not in legal:
            raise Exception("Illegal action " + str(action))
        action_type, i = action
        if action_type == COVIDRules.Actions.LOCKDOWN:
            state.data.grids[i].isLockdown = True
        elif action_type == COVIDRules.Actions.REOPEN:
            state.data.grids[i].isLockdown = False
    applyAction = staticmethod(applyAction)

class COVIDRules:
    class Actions:
        INFECT = 'Infect'
        IDLE = 'Idle'
    """
    These functions govern how govt interacts with his environment under the classic game rules.
    """
    def getLegalActions(state, agentIndex):
        """
        Returns a list of possible actions.
        """
        return [COVIDRules.Actions.INFECT, COVIDRules.Actions.IDLE]
    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action, agentIndex):
        """
        Edits the state to reflect the results of the action.
        """
        legal = COVIDRules.getLegalActions(state, agentIndex)
        if action not in legal:
            raise Exception("Illegal action " + str(action))
        cell = state.data.grids[agentIndex - 1]
        if action == COVIDRules.Actions.INFECT and cell.isLockdown:
            cell.isInfected = True
            state.data._numInfected += 1
        ngrids = len(state.data.grids)
        if agentIndex == ngrids:
            state.data.level += 1
        # if all cells were infected or reached max level
        if state.data._numInfected == ngrids or state.data.level > state.maxLevel:
            state.data.isEnd = True
    applyAction = staticmethod(applyAction)
