

from webscraping.stat_models import *
from generators.web_info import *
import random

def getRandomAction(stats: GlobalStats, website: WebPage):
    random.sample(range(4), [.5,.3,.2,.1])
    value = random.randint(0,5)
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
        pass

    def modify(self, website_state: WebSiteState):
        if self.selector is not None:
            # print(f"Valid selector found")
            website_state.website.css.add_rule(self.selector, self.rule_name, self.rule_value)
        else:
            print(f"Valid selector not found in 500 tries")

    def __str__(self):
        return f"{self.selector} {{\n\t{self.rule_name}: {self.rule_value}\n}}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.selector == other.selector and self.rule_name == other.rule_name and self.rule_value == other.rule_value

    def __hash__(self):
        return hash((self.selector, self.rule_name, self.rule_value))


class PureStatisticalAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super.__init__(stats, website)
        tries = 0
        while True:
            selector = random.choices(stats.selectors, stats.selector_freq)[0]
            while not website.contains_selector(selector):
                selector = random.choices(stats.selectors, stats.selector_freq)[0]
                tries += 1
                if tries == 100:
                    # print(f"{selector}")
                    selector = None
                    break
            self.selector = selector
            if selector in stats.tag_rule_key_map:
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
        tries = 0
        while True:
            selector = random.choice(website.html.get_tags())
            while not website.contains_selector(selector):
                selector = random.choice(website.html.get_tags())
                tries += 1
                if tries == 100:
                    selector = None
                    break
            self.selector = selector
            if selector in stats.tag_rule_key_map:
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
        tries = 0
        while True:
            selector = random.choice(website.html.get_tags())
            while not website.contains_selector(selector):
                selector = random.choice(website.html.get_tags())
                tries += 1
                if tries == 100:
                    selector = None
                    break
            self.selector = selector
            self.rule_name = WebColors.get_random_rule()
            self.rule_value = WebColors.get_random_value()
  
                  
class RandomFontAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super.__init__(stats, website)
        tries = 0
        while True:
            selector = random.choice(website.html.get_tags())
            while not website.contains_selector(selector):
                selector = random.choice(website.html.get_tags())
                tries += 1
                if tries == 100:
                    selector = None
                    break
            self.selector = selector
            self.rule_name = WebFonts.get_random_rule()
            self.rule_value = WebFonts.get_random_value()
  