from world_state import WorldState

class World:

    def __init__( self, agents ):
        self.agents = agents
        self.currAgentInd = 0      # 0 is Gov, 1 is COVID
        self.iterNum = 0
        self.gameOver = False

        self.state = WorldState()


    def printStats( self ):
        pass


    def run( self, totalIter=1000, verbose=False ):
        """
        Main control loop for game play.
        """
        while not self.gameOver:

            agent = self.agents[self.currAgentInd]

            # Generate observation of the state
            observation = agent.observationFunction(self.state)

            # Solicit actiion
            agent_actions = agent.getAction(observation)
            
            # Update state
            self.state = self.state.generateSuccessor(self.currAgentInd, action)

            # Switch players
            self.currAgentInd = (self.currAgentInd + 1) % 2
            self.iterNum += 1 if self.currAgentInd else 0

            # Print stats
            print('----------------------------------------------------------')
            print('Round: {}'.format(self.iterNum))
            print('COVID Stats: {} / {}'.format(self.state.numInfected, self.state.population))
            print('Value: {}'.format(self.state.value))

            if verbose:
                # Print any additional information
                self.printStats()

            # Game over if reach max iter or everyone has COVID
            if self.iterNum >= totalIter or self.state.allCovid():
                self.gameOver = True

