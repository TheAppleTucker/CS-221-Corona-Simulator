class WorldStateData:

    """
    Stores a list of grids: one grid for each time step.
    This grid stores:
    -the number of people in each location (and the total number of people)
    -the number of Covid cases in each location
    -whether there is a lockDown in that time step
    - whether the agent has won or lost or neither
    - the agent's score so far
    """

    def __init__(self,totalNumPeople, numRowsinWorld, numColsinWorld, numTimeSteps):

        self.createArrayOfGrids(totalNumPeople, numRowsinWorld, numColsinWorld, numTimeSteps)

    def createArrayOfGrids(self, totalNumPeople, numRows, numCols, totalTimeSteps):
        for i in range(totalTimeSteps):
            grid_i = GridData(totalNumPeople, 0, numRows, numCols)
            self.grids.append(grid_i)


class GridData:
    """
    Stores:
    -the number of people in each location (and the total number of people)
    -the number of Covid cases in each location
    -whether there is a lockDown in that time step
    - whether the agent has won or lost or neither
    - the agent's score so far

    We can also set the following:
    -the score at the current time step
    -whether the current time step indicates a win or loss state
    """
    def __init__(self, totalNumPeople, timeStep, rows, cols):
        if(timeStep == 0):
            self.isLockdown = False
            self.numPeopleAlive = totalNumPeople
            self.numCovidCases = 0
            self.score = 0
            self.grid = []
            self.lockdownLocations = []
            grid_row_list = []
            for row in range(rows):
                for col in range(cols):
                    grid_row_list.append(LocationData(row,col))
            self.has_won = False
            self.has_lost = False
            self.score = 0

        else:
            for row in range(rows):
                for col in range(cols):
                    loc = LocationData(row, col)
                    if(loc.isLockdown):
                        self.isLockdown = True
                        (self.lockdownLocations).append(loc)
                    if(loc.isInfected):
                        self.numCovidCases += loc.numPeopleInLoc
                    self.numPeopleAlive += loc.numPeopleInLoc

    def setScore(self, newScore):
        self.score = newScore

    def setWon(self):
        self.has_won = True

    def setLost(self):
        self.has_lost = True


class LocationData:
    """
    Stores data about a given location in the grid:
    This includes:
    - The number of people in the grid
    - Whether there is a lockdown imposed in this location
    - Whether the people in this grid are infected

    We can also set the following:
    -whether there is a lockdown in the location
    -the number of people in each location
    -whether the people in the location are cured of COVID
    """

    def __init__(self, timeStep, row, col):
        self.pos = (row, col)
        self.timeStep = timeStep
        # I have taken DEFAULT_NUM_PEOPLE_IN_LOC = 2; we can put another number if we'd like
        self.numPeopleInLoc = 2
        self.isInfected = False
        self.isLockdown = False

    def setLockdown(self, timeStep):
        self.isLockdown = True
        self.timeStep = timeStep

    def setNumPeopleInLoc(self, newNumPeople, timeStep):
        self.numPeopleInLoc = newNumPeople
        self.timeStep = timeStep

    def setCured(self, timeStep):
        self.isInfected = False
        self.timeStep = timeStep




