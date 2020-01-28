from copy import deepcopy, copy
from mcts import mcts
from functools import reduce
import operator
from webscraping.web_scraper import *

class CSS():
    def __init__(self, rules):
        self.rules = rules
    
    def evaluate(self):
        # TODO: Evaluate the rules based on some criteria
        return 1

class WebSite():
    photo_eval_limit = .5
    css_eval_limit = .7

    def __init__(self, url=None, html=None):
        if html is not None:
            self.html = html
            self.css = CSS(rules=[])
        else:
            self.html, css = scrape(url)
            self.css = CSS(rules=css)

    def gen_photo(self):
        # TOOD: Generate photo from HTML & the new CSS
        return None

    def evaluate_photo(self):
        photo = self.gen_photo()
        # TODO: Evaluate a photo based on some criteria
        return 1

    def evaluate_css(self):
        return self.css.evaluate()

    def evaluate(self):
        css_evaluation = self.evaluate_css()
        if css_evaluation < WebSite.css_eval_limit:
            return 0
        else:
            photo_evaluation = self.evaluate_photo()
            return css_evaluation*.2 + photo_evaluation*.8

    def __str__(self):
        return str((self.html, self.css))

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memo): #Pass a reference to the original HTML but create a copy of the css 
        ws = WebSite(html=self.html)
        ws.css = copy(self.css)
        return ws
           
class WebSiteState():
    min_acceptable_evaluation = .5
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
        return self.website.evaluate() < min_acceptable_evaluation

    def getReward(self): # Return Number between 0-1 or False
        return self.website.evaluate()

class Action():
    # TODO: Define actions we can take in this space, could be genetic or based on the stats we gathered
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