import random
import copy

random.seed(876)

class WorldStateData:

    class GridData:
        def __init__(self, numPeople, numInfected, susceptiblityCoef):
            self.numPeople = numPeople
            self.numCovidCases = numInfected
            # chance of infection / num person infected
            self.susceptiblityCoef = susceptiblityCoef
            self.isLockedDown = False

        @classmethod
        def createGrids(cls, numGrids):
            initGridInfectedRatio = 0.1
            maxGridsInfected = max(1, int(numGrids * initGridInfectedRatio))
            gridsInfected = set(int(random.uniform(0, numGrids)) for _ in range(maxGridsInfected))
            grids = []
            for i in range(numGrids):
                numPeople = random.randint(20, 50)
                susceptiblityCoef = random.uniform(0.05, 0.01)
                numInfected = 1 if i in gridsInfected else 0
                grids.append(cls(numPeople, numInfected, susceptiblityCoef))
            return grids

        def toggleLockdown(self):
            if self.isLockedDown:
                self.isLockedDown = False
            else:
                self.isLockedDown = True

        def numHealthy(self):
            healthy = self.numPeople - self.numCovidCases
            return healthy if healthy > 0 else 0
        
    def __init__(self, prevData=None, numGrids=100):
        if prevData is not None:
            self.grids = copy.deepcopy(prevData.grids)
            self.numGrids = prevData.numGrids
            self.numInfected = prevData.numCovidCases()
            self.level = prevData.level
            self.score = prevData.score
            self.population = prevData.population
            self.isEnd = prevData.isEnd
        else:
            self.grids = WorldStateData.GridData.createGrids(numGrids)
            self.numGrids = numGrids
            self.numInfected = self.numCovidCases()
            self.level = 0
            self.score = 0
            self.population = self.totalPopulation()
            self.isEnd = False

    def totalPopulation(self):
        total = sum([grid.numPeople if grid.numPeople else 0 for grid in self.grids])
        return total

    def numCovidCases(self):
        total = sum([grid.numCovidCases if grid.numCovidCases else 0 for grid in self.grids])
        return total

    def numLockdowns(self):
        total = sum([1 if grid.isLockedDown else 0 for grid in self.grids])
        return total

    def numGridsInfected(self):
        total = sum([1 if grid.numCovidCases > 0 else 0 for grid in self.grids])
        return total

    def allInfected(self):
        return self.numCovidCases() == self.totalPopulation()
         
