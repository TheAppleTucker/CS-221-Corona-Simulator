from world_state import WorldState
from agents import GovernmentAgent, COVIDAgent

class World:

    def __init__(self, agents, totalIter=100):
        self.agents = agents
        self.numAgents = len(agents)
        self.currAgentInd = 0         # 0 is Gov, 1 is COVID
        self.iterNum = 0
        self.totalIter = totalIter
        self.gameOver = False
        self.state = WorldState(None, self.numAgents, totalIter)

    def printStats( self ):
        pass

    def run(self, verbose=False):
        """
        Main control loop for game play.
        """
        while not self.gameOver:

            agent = self.agents[self.currAgentInd]

            # For Govt, this returns list of tuples (ACTION, LIST_INDEX)
            # For COVID, this returns list of 2 items [INFECT, IDLE]
            #legalActions =  self.state.getLegalActions(self.currAgentInd)

            # Solicit actiion
            #action = agent.getAction(self.state.deepCopy(), legalActions)
            #action = agent.getAction(self.state.deepCopy())
            action = agent.getAction(self.state)

            # Update state
            self.state = self.state.generateSuccessor(self.currAgentInd, action)

            # Print stats
            if self.currAgentInd == 0:
              print('----------------------------------------------------------')
              print('Round: {}'.format(self.iterNum))
              print('Num People Infected: {} / {}'.format(self.state.data.numCovidCases(), self.state.data.population))
              print('Num States Infected: {} / {}'.format(self.state.data.numGridsInfected(), len(self.state.data.grids)))
              print('Lockdown Stats: {} / {}'.format(self.state.data.numLockdowns(), len(self.state.data.grids)))
              print('Value: {}'.format(self.state.data.score))

              if verbose:
                  # Print any additional information
                  self.printStats()

            # Switch players
            self.currAgentInd = (self.currAgentInd + 1) % self.numAgents
            self.iterNum += 1 if not self.currAgentInd else 0

            # Game over if reach max iter or everyone has COVID
            if self.iterNum >= self.totalIter or self.state.data.allInfected():
                self.gameOver = True

if __name__ == '__main__':
    agents = [GovernmentAgent()] + [COVIDAgent() for _ in range(50)]
    world = World(agents, 50)
    world.run()

