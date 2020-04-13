from copy import deepcopy, copy
from mcts import mcts
from webscraping.web_scraper import *
from webscraping.stat_models import *
import shutil
import os
from generators.actions import *

branching_factor = 30
single_run_max_depth = 20
single_run_num_rollouts = 10  # 20
total_depth = 15 #200

class WebSiteState:
    min_acceptable_evaluation = .5
    def __init__(self, url, stats, cleaned=False):
        self.website = WebPage(url=url, cleaned=cleaned)
        self.stats = stats
        self.depth = 1
        self.possibleActions = None
        self.evaluation = None

    def getPossibleActions(self):
        if self.possibleActions is None: 
            self.possibleActions = [getRandomAction(self.stats, self.website) for _ in range(branching_factor)]
        return self.possibleActions

    def takeAction(self, action, depthOverride=None):
        newState = deepcopy(self)
        action.modify(newState)
        if depthOverride is not None:
            newState.depth = depthOverride
            newState.possibleActions = None
            newState.evaluation = None
            # print("Override on depth")
        else:
            newState.depth += 1
            newState.possibleActions = None
            newState.evaluation = None
        return newState

    def isTerminal(self):
        # print("Reached terminal state")
        return self.depth == single_run_max_depth
        # return self.website.evaluate() < WebSiteState.min_acceptable_evaluation

    def getReward(self):  # Return Number between 0-1 or False
        if self.evaluation is None:
            self.evaluation = self.website.evaluate()
        # else:
        #     print("Reward called multiple times")
        return self.evaluation

    def __str__(self):
        return f"Depth: {self.depth} Website: {self.website}"

def customPolicy(state):
    action = random.choice(state.getPossibleActions())
    state = state.takeAction(action)
    return state.getReward()

def main(school):
    depth = 0
    montecarlosearch = mcts(iterationLimit=single_run_num_rollouts, rolloutPolicy=customPolicy)
    directory = f"results/{school}"
    images_dir = f"images/html_images"
    os.makedirs(directory, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    shutil.rmtree(directory)
    shutil.rmtree(images_dir)
    os.makedirs(directory, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    stats = GlobalStats()
    # print(stats.data["tag_freq"]["p"])
    initialState = WebSiteState(url=school, stats=stats)
    initialState.website.download_imgs()
    initialState.website.gen_photo(f"{directory}/initial_screenshot.png")
    while depth < total_depth:
        print(f"Depth: {depth}")
        action = montecarlosearch.search(initialState=initialState)
        # print(f"Depth: {depth} done")
        action.save(f"{directory}/actions.txt")
        initialState = initialState.takeAction(action, depthOverride=0)
        initialState.getReward()
        if depth % 1 == 0:
            initialState.website.gen_photo(f"{directory}/screenshot_{depth}.png")
        depth += 1
        montecarlosearch = mcts(iterationLimit=single_run_num_rollouts, rolloutPolicy=customPolicy)
    initialState.website.gen_photo(f"{directory}/final_screenshot.png")
    print("Finished")


if __name__ == '__main__':
    scraper.set_desktop_view()
    school = "mit"
    main(school)
    
