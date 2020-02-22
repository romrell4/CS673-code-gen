

from webscraping.stat_models import *
from generators.web_info import *
from generators.mcts_generator import WebSiteState
import random


def getRandomAction(stats: GlobalStats, website: WebPage):
    value = random.choices(range(4), [.5,.3,.2,.1])[0]
    if value == 0:
        return RandomColorAction(stats, website)
    elif value == 1:
        return RandomFontAction(stats, website)
    elif value == 2:
        return WebSiteSpecificSelectorModifier(stats, website)
    else:
        return PureStatisticalAction(stats, website)

class Action:
    # TODO: Define actions we can take in this space, could be genetic or based on the stats we gathered
    def __init__(self, stats: GlobalStats, website: WebPage):
        self.max_tries = 1000
        self.tries = 0
        self.selector = None
        self.rule_name = ""
        self.rule_value = ""

    def modify(self, website_state: WebSiteState):
        if self.selector is not None:
            # print(f"Valid selector found")
            website_state.website.css.add_rule(self.selector, self.rule_name, self.rule_value)
        else:
            print(f"Valid selector not found in {self.max_tries} tries")

    def __str__(self):
        return f"{self.selector} {{\n\t{self.rule_name}: {self.rule_value}\n}}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.selector == other.selector and self.rule_name == other.rule_name and self.rule_value == other.rule_value

    def __hash__(self):
        if self.selector is None:
            return hash((self.rule_name, self.rule_value))
        return hash((self.selector, self.rule_name, self.rule_value))


class PureStatisticalAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super.__init__(stats, website)
        while True:
            selector = random.choice(list(website.css.selectors.keys()))
            # selector = random.choices(stats.selectors, stats.selector_freq)[0]
            while not website.contains_selector(selector):
                selector = random.choice(list(website.css.selectors.keys()))
                # selector = random.choices(stats.selectors, stats.selector_freq)[0]
                self.tries += 1
                if self.tries == self.max_tries:
                    # print(f"{selector}")
                    selector = None
                    break
            self.selector = selector
            if selector is not None and selector in stats.tag_rule_key_map:
                self.rule_name = random.choices(stats.tag_rule_key_map[selector][0],
                                                stats.tag_rule_key_map[selector][1])[0]
                self.rule_value = random.choices(stats.rule_key_value_map[self.rule_name][0],
                                                  stats.rule_key_value_map[self.rule_name][1])[0]
                break
            else:
                continue


class WebSiteSpecificSelectorModifier(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super.__init__(stats, website)
        while True:
            selector = random.choice(list(website.css.selectors.keys()))
            while not website.contains_selector(selector):
                selector = random.choice(list(website.css.selectors.keys()))
                self.tries += 1
                if self.tries == self.max_tries:
                    selector = None
                    break
            self.selector = selector
            if selector is not None and selector in stats.tag_rule_key_map:
                self.rule_name = random.choices(stats.tag_rule_key_map[selector][0],
                                                stats.tag_rule_key_map[selector][1])[0]
                self.rule_value = random.choices(stats.rule_key_value_map[self.rule_name][0],
                                                  stats.rule_key_value_map[self.rule_name][1])[0]
                break
            else:
                continue


class RandomColorAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super.__init__(stats, website)
        selector = random.choice(list(website.css.selectors.keys()))
        while not website.contains_selector(selector):
            selector = random.choice(list(website.css.selectors.keys()))
            self.tries += 1
            if self.tries == self.max_tries:
                selector = None
                break
        self.selector = selector
        self.rule_name = WebColors.get_random_rule()
        self.rule_value = WebColors.get_random_value()
  
                  
class RandomFontAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super.__init__(stats, website)
        selector = random.choice(list(website.css.selectors.keys()))
        while not website.contains_selector(selector):
            selector = random.choice(list(website.css.selectors.keys()))
            self.tries += 1
            if self.tries == self.max_tries:
                selector = None
                break
        self.selector = selector
        self.rule_name = WebFonts.get_random_rule()
        self.rule_value = WebFonts.get_random_value(self.rule_name)
            
  