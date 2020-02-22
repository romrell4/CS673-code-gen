from copy import deepcopy, copy
from mcts import mcts
from webscraping.web_scraper import *
from webscraping.stat_models import *
import shutil
import os
from generators.actions import *

class WebSiteState:
    min_acceptable_evaluation = .5
    def __init__(self, url, stats, cleaned=True):
        self.website = WebPage(url=url, cleaned=cleaned)
        self.stats = stats
        self.depth = 1

    def getPossibleActions(self):
        possibleActions = [getRandomAction(self.stats, self.website) for _ in range(5)]
        return possibleActions

    def takeAction(self, action, depthOverride=None):
        newState = deepcopy(self)
        action.modify(newState)
        if depthOverride is not None:
            newState.depth = depthOverride
            # print("Override on depth")
        else:
            newState.depth += 1
        return newState

    def isTerminal(self):
        return self.depth == 10
        # return self.website.evaluate() < WebSiteState.min_acceptable_evaluation

    def getReward(self): # Return Number between 0-1 or False
        return self.website.evaluate()

    def __str__(self):
        return f"Depth: {self.depth} Website: {self.website}"


def main(school):
    depth = 0
    montecarlosearch = mcts(timeLimit=.5)
    directory = f"results/{school}"
    shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)
    stats = GlobalStats()
    # print(stats.data["tag_freq"]["p"])
    initialState = WebSiteState(url=school, stats=stats)
    # photo = initialState.website.gen_photo("screenshot.png")
    while depth < 400:
        action = montecarlosearch.search(initialState=initialState)
        action.save(f"results/{school}/actions.txt")
        initialState = initialState.takeAction(action, depthOverride=0)
        initialState.getReward()
        if depth % 25 == 0:
            initialState.website.gen_photo(f"{directory}/screenshot_{depth}.png")
        depth += 1
    photo = initialState.website.gen_photo(f"{directory}/final_screenshot.png")
    print("Finished")


if __name__ == '__main__':
    school = "byu"
    main(school)
    