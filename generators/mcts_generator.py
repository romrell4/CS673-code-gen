from copy import deepcopy, copy
from mcts import mcts
from webscraping.web_scraper import *
from webscraping.stat_models import *
from one_time_scripts.generate_global_stats import Stats
class WebSiteState:
    min_acceptable_evaluation = .5
    def __init__(self, url, stats):
        self.website = WebPage(url=url)
        self.stats = stats
        self.depth = 1

    def getPossibleActions(self):
        possibleActions = [Action(self.stats, self.website) for _ in range(5)]
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        action.modify(newState)
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
    def __init__(self, stats, website):
        tries = 0
        selector = random.choices(stats.selectors, stats.selector_freq)[0]
        while not website.containsSelector(selector):
            selector = random.choices(stats.selectors, stats.selector_freq)[0]
            tries += 1
            if tries == 10000:
                # print(f"{selector}")
                selector = None
                break
        self.selector = selector
        self.ruleName = random.choices(stats.rule_names, stats.rule_freqs)[0]
        self.ruleValue = random.choices(list(stats.rule_values[self.ruleName].keys()), list(stats.rule_values[self.ruleName].values()))[0]

    def modify(self, websiteState):
        if self.selector is not None:
            # print(f"Valid selector found")
            websiteState.website.css.addRule(self.selector, self.ruleName, self.ruleValue)
        else:
            print(f"Valid selector not found in 500 tries")

    def __str__(self):
        return str((0, 1))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return False

    def __hash__(self):
        return hash((0))



def main(school):
    stats = Stats.read("../resources/global_stats.json")
    print(stats.data["tag_freq"]["p"])
    initialState = WebSiteState(url=school, stats=stats)
    # print(stats.rule_frequency)
    print(stats.selector_freq)
    # photo = initialState.website.gen_photo("screenshot.png")
    depth = 0
    montecarlosearch = mcts(timeLimit=1)
    directory = f"results/{school}"
    os.makedirs(directory, exist_ok=True)
    while depth < 100:
        action = montecarlosearch.search(initialState=initialState)
        initialState = initialState.takeAction(action)
        initialState.getReward()
        initialState.website.gen_photo(f"{directory}/screenshot_{depth}.png")
        depth += 1
    photo = initialState.website.gen_photo(f"{directory}/final_screenshot.png")
    print("Finished")


if __name__ == '__main__':
    school = "byu"
    main(school)
    