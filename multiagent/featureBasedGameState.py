# from pacman import GameState
from util import euclidean_distance

class FeatureBasedGameState(object):
    def __init__(self, gameState):
        # type: (GameState) -> None

        # Storing the GameState; it might be needed
        self.rawGameState = gameState

        # Please list all the features here. It becomes convenient; don't miss out any, or directly initialise elsewhere
        self.isClosestGhost1UnitNorth = None
        self.isClosestGhost1UnitWest = None
        self.isClosestGhost1UnitSouth = None
        self.isClosestGhost1UnitEast = None

        # Caching some stuff for faster calculations - don't change this please!
        self.closestGhosts = None

        # This is where you will calculate the features you have listed above
        pacmanPosition = self.rawGameState.getPacmanPosition()
        self.isClosestGhost1UnitNorth = self.doesGhostExist(pacmanPosition, 'North', 1)
        self.isClosestGhost1UnitWest = self.doesGhostExist(pacmanPosition, 'West', 1)
        self.isClosestGhost1UnitSouth = self.doesGhostExist(pacmanPosition, 'South', 1)
        self.isClosestGhost1UnitEast = self.doesGhostExist(pacmanPosition, 'East', 1)


    def findClosestGhosts(self):
        "There can be multiple closest ghosts. So this returns a list of tuples. Eg. [(1,1), (5,4)]"
        if self.closestGhosts is not None:
            return self.closestGhosts
        pacmanPosition = self.rawGameState.getPacmanPosition()
        ghostPositions = self.rawGameState.getGhostPositions()
        minDistance = 999999999
        closestGhosts = []
        for ghostPosition in ghostPositions:
            ghostDistance = euclidean_distance(pacmanPosition, ghostPosition)
            if ghostDistance < minDistance:
                closestGhosts = [ghostPosition]
                minDistance = ghostDistance
            elif ghostDistance == minDistance:  # TODO: this might be problematic - floating point equality comparison
                closestGhosts.append(ghostPosition)
        self.closestGhosts = closestGhosts
        return self.closestGhosts

    def doesGhostExist(self, currentPos, direction, distance):
        "Find if a ghost exists in a certain direction from the given position: doesGhostExist((2,3), 'North', 1)"
        closestGhosts = self.findClosestGhosts()
        x, y = currentPos
        if direction == 'North':
            return (x, y+distance) in closestGhosts
        elif direction == 'West':
            return (x-distance, y) in closestGhosts
        elif direction == 'South':
            return (x, y-distance) in closestGhosts
        elif direction == 'East':
            return (x+distance, y) in closestGhosts
        else:
            raise Exception("You have provided an invalid direction: ", direction)

    def __key(self):
        return (self.isClosestGhost1UnitNorth,
                self.isClosestGhost1UnitEast,
                self.isClosestGhost1UnitSouth,
                self.isClosestGhost1UnitWest
                )

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, FeatureBasedGameState):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return str({
            "isClosestGhost1UnitNorth": self.isClosestGhost1UnitNorth,
            "isClosestGhost1UnitWest": self.isClosestGhost1UnitWest,
            "isClosestGhost1UnitSouth": self.isClosestGhost1UnitSouth,
            "isClosestGhost1UnitEast": self.isClosestGhost1UnitEast
        })