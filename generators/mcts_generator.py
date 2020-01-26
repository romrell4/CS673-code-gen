from copy import deepcopy, copy
from mcts import mcts
from functools import reduce
import operator
from webscraping.web_scraper import *

class CSS():
    def __init__(self, rules):
        self.rules = rules

class WebSite():
    def __init__(self, url=None, html=None):
        if html is not None:
            self.html = html
            self.css = CSS(rules=[])
        else:
            self.html, css = scrape(url)
            self.css = CSS(rules=css)
    
    def __str__(self):
        return str((self.html, self.css))

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memo): #Pass a reference to the original HTML but create a copy of the css 
        ws = WebSite(html=self.html)
        ws.css = copy(self.css)
        return ws

class WebSiteState():
    def __init__(self, url):
        self.website = WebSite(url=url)
        self.depth = 1

    def getPossibleActions(self):
        possibleActions = [Action()]
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.depth += 1
        return newState

    def isTerminal(self):
        return self.depth == 5

    def getReward(self): # Return Number between 0-1 or False
        return False


class Action():
    def __init__(self):
        pass

    def __str__(self):
        return str((0, 1))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return False

    def __hash__(self):
        return hash((0))

initialState = WebSiteState(url="test.html")
mcts = mcts(timeLimit=1000)
action = mcts.search(initialState=initialState)

print(action)
print("Finished")