
import typing
from webscraping.stat_models import *
from generators.web_info import *
from generators.mcts_generator import WebSiteState
import random
import requests
import time


def getRandomAction(stats: GlobalStats, website: WebPage):
    return BrandArchetypeAction(stats, website)
    value = random.choices(range(4), [.5, .3, .2, .1])[0]
    if value == 0:
        return RandomColorAction(stats, website)
    elif value == 1:
        return RandomFontAction(stats, website)
    elif value == 2:
        return WebSiteSpecificSelectorModifier(stats, website)
    else:
        return WebSiteSpecificSelectorModifier(stats, website)


class Action:
    # TODO: Define actions we can take in this space, could be genetic or based on the stats we gathered
    def __init__(self, stats: GlobalStats, website: WebPage):
        self.max_tries = 1000
        self.tries = 0
        self.selector = None
        self.rule_name = ""
        self.rule_value = ""
        self.rule_links = None
        self.mutations = None

    def modify(self, website_state: WebSiteState):
        if self.selector is not None:  # An add action
            # print(f"Valid selector found")
            # Add rule just mutates any existing rule
            website_state.website.css.add_rule(self.selector, self.rule_name, self.rule_value)
            website_state.website.html.add_link(self.rule_links)
        elif self.mutations is not None:
            for mutation, links in self.mutations:
                scope, selector, rule, value = mutation
                website_state.website.css.add_rule(selector, rule, value, scope=scope)
                website_state.website.html.add_link(links)
        else:
            print(f"Valid selector not found in {self.max_tries} tries")

    def __str__(self):
        if self.selector is not None:
            return f"{self.selector} {{\n\t{self.rule_name}: {self.rule_value};\n}}\n"
        elif self.mutations is not None:
            string = ""
            for mutation, links in self.mutations:
                scope, selector, rule, value = mutation
                string += f"{selector} {{\n\t{rule}: {value};\n}}\n"
            return string
        else:
            return "No mutation\n"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.selector == other.selector and self.rule_name == other.rule_name and \
               self.rule_value == other.rule_value

    def save(self, filename):
        with open(filename, 'a+') as f:
            f.write(str(self))

    def __hash__(self):
        if self.selector is None:
            return hash((self.rule_name, self.rule_value))
        return hash((self.selector, self.rule_name, self.rule_value))


class PureStatisticalAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)
        while True:
            # selector = random.choice(list(website.css.selectors.keys()))
            selector = random.choices(stats.tag_map[0], stats.tag_map[1])[0]
            while not website.contains_selector(selector):
                # selector = random.choice(list(website.css.selectors.keys()))
                selector = random.choices(stats.tag_map[0], stats.tag_map[1])[0]
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
        super().__init__(stats, website)
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
        super().__init__(stats, website)
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
        super().__init__(stats, website)
        selector = random.choice(list(website.css.selectors.keys()))
        while not website.contains_selector(selector):
            selector = random.choice(list(website.css.selectors.keys()))
            self.tries += 1
            if self.tries == self.max_tries:
                selector = None
                break
        self.selector = selector
        self.rule_name = webFonts.get_random_rule()
        self.rule_value = webFonts.get_random_value(self.rule_name)
        self.rule_links = webFonts.get_rule_links(self.rule_value)


class MutateColorSchemeAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None
        
        num_colors = len(colors.items())
        new_color = WebColors.get_random_value_array()
        inputs = [new_color]
        new_colors = None
        print(inputs)
        while new_colors is None:
            r = requests.post('http://colormind.io/api/', json={"input": inputs, "model": "ui"})
            if r.status_code != 200:
                time.sleep(1000) # Don't spam the API
                print("No Color response")
                continue
            else:
                print(r.text)
                new_colors = [f"rgb({color[0]},{color[1]},{color[2]})" for color in r.json()['result']]
        # Assign each color to a new color that is interesting
        i = 0
        for color, newColor in colors.items():
            # print(f'Colors: {color}')
            n = i % 5
            colors[color] = new_colors[n]
            i += 1

        # Make them into variables or some way to mutate all of them at once
        # TODO: Maybe make a second version of this that chooses color based on Images (or alters images)
        self.mutations = []
        for scope, selector, rule, color in website.css.background_colors():
            newcolor = colors[color]
            self.mutations.append(((scope, selector, rule, newcolor), []))

        # TODO: Add the concept of foreground & background contrast
        # Possible Ideas: 
        # * Always have foreground be Black and White & Background changes


class BrandArchetypeAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None

        num_colors = len(colors.items())
        # TODO: Pass in website name somehow
        new_color = archetypes.get_color('byu')
        inputs = [new_color]
        new_colors = None
        print(inputs)
        while new_colors is None:
            r = requests.post('http://colormind.io/api/', json={"input": inputs, "model": "ui"})
            if r.status_code != 200:
                time.sleep(1000)  # Don't spam the API
                print("No Color response")
                continue
            else:
                print(r.text)
                new_colors = [f"rgb({color[0]},{color[1]},{color[2]})" for color in r.json()['result']]
        # Assign each color to a new color that is interesting
        i = 0
        for color, newColor in colors.items():
            # print(f'Colors: {color}')
            n = i % 5
            colors[color] = new_colors[n]
            i += 1

        # Make them into variables or some way to mutate all of them at once
        # TODO: Maybe make a second version of this that chooses color based on Images (or alters images)
        self.mutations = []
        for scope, selector, rule, color in website.css.background_colors():
            newcolor = colors[color]
            self.mutations.append(((scope, selector, rule, newcolor), []))

        # TODO: Add the concept of foreground & background contrast
        # Possible Ideas:
        # * Always have foreground be Black and White & Background changes

        # Fonts
        newfont, link = archetypes.get_font_and_link('byu')
        for scope, selector, rule, font in website.css.fonts():
            self.mutations.append(((scope, selector, rule, newfont), link))
