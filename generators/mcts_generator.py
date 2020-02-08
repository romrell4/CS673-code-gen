from copy import deepcopy, copy
from mcts import mcts
from webscraping.web_scraper import *
from webscraping.stat_models import *
import shutil
from one_time_scripts.generate_global_stats import GlobalStats
class WebSiteState:
    min_acceptable_evaluation = .5
    def __init__(self, url, stats):
        self.website = WebPage(url=url)
        self.stats = stats
        self.depth = 1

    def getPossibleActions(self):
        possibleActions = [Action(self.stats, self.website) for _ in range(5)]
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
        return self.website.evaluate() < WebSiteState.min_acceptable_evaluation

    def getReward(self): # Return Number between 0-1 or False
        return self.website.evaluate()

    def __str__(self):
        return f"Depth: {self.depth} Website: {self.website}"

class Action:
    # TODO: Define actions we can take in this space, could be genetic or based on the stats we gathered
    def __init__(self, stats, website):
        tries = 0
        selector = random.choices(stats.selectors, stats.selector_freq)[0]
        selector = random.choice(list(website.css.selectors.keys()))
        while not website.containsSelector(selector):
            selector = random.choices(stats.selectors, stats.selector_freq)[0]
            selector = random.choice(list(website.css.selectors.keys()))
            tries += 1
            if tries == 100:
                # print(f"{selector}")
                selector = None
                break
        self.selector = selector
        self.ruleName = random.choices(stats.rule_names, stats.rule_freqs)[0]
        self.ruleValue = random.choices(list(stats.rule_values[self.ruleName].keys()), list(stats.rule_values[self.ruleName].values()))[0] + "!important"

    def modify(self, websiteState):
        if self.selector is not None:
            # print(f"Valid selector found")
            websiteState.website.css.addRule(self.selector, self.ruleName, self.ruleValue)
        else:
            print(f"Valid selector not found in 500 tries")

    def __str__(self):
        return f"{self.selector} {{\n\t{self.ruleName}: {self.ruleValue}\n}}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.selector == other.selector and self.ruleName == other.ruleName and self.ruleValue == other.ruleValue

    def __hash__(self):
        return hash((self.selector, self.ruleName, self.ruleValue))



def main(school):
    stats = GlobalStats()
    # print(stats.data["tag_freq"]["p"])
    initialState = WebSiteState(url=school, stats=stats)
    # print(stats.rule_frequency)
    # print(stats.selector_freq)
    # photo = initialState.website.gen_photo("screenshot.png")
    depth = 0
    montecarlosearch = mcts(timeLimit=1)
    directory = f"results/{school}"
    shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)
    while depth < 1000:
        action = montecarlosearch.search(initialState=initialState)
        # print(action)
        initialState = initialState.takeAction(action, depthOverride=0)
        initialState.getReward()
        if depth % 50 == 0:
            initialState.website.gen_photo(f"{directory}/screenshot_{depth}.png")
        depth += 1
    photo = initialState.website.gen_photo(f"{directory}/final_screenshot.png")
    print("Finished")


if __name__ == '__main__':
    school = "byu"
    main(school)
    