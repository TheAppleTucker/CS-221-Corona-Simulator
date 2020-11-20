from world_state import GovtRules, COVIDRules

class GovernmentAgent:

    def __init__(self):
        pass

    def getAction(self, state):
        #return self._lockDownFirstGridSeen(state)
        #return self._idle(state)
        return self._lockDownMostSusceptible(state)

    def _lockDownFirstGridSeen(self, state):
        for ind, grid in enumerate(state.data.grids):
            if not grid.isLockedDown:
                return GovtRules.Actions.LOCKDOWN, ind
        return GovtRules.Actions.IDLE, -1

    def _lockDownMostSusceptible(self, state):
        susceptibility = []
        for ind, grid in enumerate(state.data.grids):
            if not grid.isLockedDown:
                susceptibility.append((ind, grid.susceptiblityCoef * grid.numHealthy()))

        if len(susceptibility) == 0:
            return GovtRules.Actions.IDLE, -1
    
        sorted_vals = sorted(susceptibility, key=lambda x: x[1], reverse=True)
        return GovtRules.Actions.LOCKDOWN, sorted_vals[0][0]

    def _idle(self, state):
        return GovtRules.Actions.IDLE, -1

class COVIDAgent:

    def __init__(self):
        pass

    def getAction(self, state):
        # Always want to infect
        return COVIDRules.Actions.INFECT

