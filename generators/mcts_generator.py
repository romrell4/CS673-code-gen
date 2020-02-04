from copy import deepcopy, copy
from mcts import mcts
from functools import reduce
import operator
from webscraping.web_scraper import *
from webscraping.stat_models import *

class WebSiteState:
    min_acceptable_evaluation = .5
    def __init__(self, url):
        self.website = WebPage(url=url)
        self.depth = 1

    def getPossibleActions(self):
        # TODO: Create different actions based on the level of the tree we are in. (i.e. large changes at the beginning and smaller later on -- temperature based mutations essentially)
        possibleActions = [Action(), Action(), Action()]
        return possibleActions

    def takeAction(self, action):
        # TODO: Take the action into account here
        newState = deepcopy(self)
        action(newState)
        newState.depth += 1
        return newState

    def isTerminal(self):
        return self.website.evaluate() < WebSiteState.min_acceptable_evaluation

    def getReward(self): # Return Number between 0-1 or False
        return self.website.evaluate()

    def __str__(self):
        return f"Depth: {self.depth} Website: {self.website}"

class Action:
    # TODO: Define actions we can take in this space, could be genetic or based on the stats we gathered
    def __init__(self):
        pass

    def __call__(self, state:WebSiteState):
        pass

    def __str__(self):
        return str((0, 1))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return False

    def __hash__(self):
        return hash((0))

initialState = WebSiteState(url="byu")
photo = initialState.website.gen_photo("screenshot.png")

print(str(initialState))
mcts = mcts(timeLimit=1)
action = mcts.search(initialState=initialState)
print("Finished")