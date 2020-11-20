import random
from world_state_data import WorldStateData

random.seed(876)

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
        state = WorldState(self)

        if agentIndex == 0:
            GovtRules.applyAction(state, action)
        else:
            COVIDRules.applyAction(state, action, agentIndex)

        #state.data.score += state.data._numInfected
        state.data.score += state.data.numInfected
        return state

    def isEnd(self):
        return self.data.isEnd

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################
    #def __init__(self, prevState = None, maxLevel = 10, numGrids):
    def __init__(self, prevState = None, numGrids=100, maxLevel = 100):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState is not None: # Initial state
            self.data = WorldStateData(prevState.data, prevState.numGrids)
            self.numGrids = prevState.numGrids
            self.maxLevel = prevState.maxLevel
        else:
            self.data = WorldStateData(None, numGrids)
            self.numGrids = numGrids
            self.maxLevel = maxLevel

    def deepCopy(self):
        state = WorldState (self)
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
                    if not state.data.grids[i].isLockedDown]
        reopen = [(GovtRules.Actions.REOPEN, i) for i in range(ngrids) \
                if state.data.grids[i].isLockedDown]
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
        if action_type == GovtRules.Actions.LOCKDOWN:
            state.data.grids[i].isLockedDown = True
        elif action_type == GovtRules.Actions.REOPEN:
            state.data.grids[i].isLockedDown = False

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
        if action == COVIDRules.Actions.INFECT and not cell.isLockedDown:
            # we should consider nearby cells but weight them down based on distance (currently only consider dist <= 1)
            left = 0 if agentIndex - 2 < 0 else \
                                state.data.grids[agentIndex - 2].numCovidCases * state.data.grids[agentIndex - 2].susceptiblityCoef
            right = 0 if agentIndex >= len(state.data.grids) else \
                                state.data.grids[agentIndex].numCovidCases * state.data.grids[agentIndex].susceptiblityCoef
            infectChance = cell.numCovidCases * cell.susceptiblityCoef + (0.1) * (left + right)
            newCovidCases = sum(int(random.random() <= infectChance) for _ in range(cell.numHealthy()))
            cell.numCovidCases = min(cell.numCovidCases + newCovidCases, cell.numPeople)

        ngrids = len(state.data.grids)
        if agentIndex == ngrids:
            state.data.level += 1

        # if all people in cells were infected or reached max level
        if state.data.allInfected() or state.data.level > state.maxLevel:
            state.data.isEnd = True

    applyAction = staticmethod(applyAction)
