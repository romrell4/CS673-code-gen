import re
import typing 
from typing import List
from webscraping.stat_models import *
from generators.web_info import *
from generators.mcts_generator import WebSiteState
from generators.palette_generator import generate_pallete_from_imgs, generate_pallete_from_random_img
import random
import requests
import time
import shutil

def getRandomAction(stats: GlobalStats, website: WebPage):
    # return ColorSchemeFromImageAction(stats, website)
    action_types = {
        RandomColorAction: True,
        RandomFontAction: False,
        WebSiteSpecificSelectorModifier: False,
        StrategicColorSchemeAction: False,
        ColorSchemeFromAllImagesAction: True,
        BrandArchetypeAction: True,
        ColorSchemeFromImageAction: True,
        MutateColorSchemeAction: True,
        MutatePageLayout: False,
        MutateElementLayout: False
    }
    action = random.choices(list(action_types.items()), [.1, .2, .1, .2, .2, .2, 0.2, 0.2, 0.05, 0.1])[0]
    if action[1]:
        return action[0](stats, website, withAlpha=True)
    return action[0](stats, website)


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

    def save(self, filename):
        with open(filename, 'a+') as f:
            f.write(str(self))


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
    def __init__(self, stats: GlobalStats, website: WebPage, withAlpha: bool=True):
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
        self.rule_value = WebColors.as_string(WebColors.get_random_value_array(), withAlpha=withAlpha)


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
    def __init__(self, stats: GlobalStats, website: WebPage, withAlpha:bool=False):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None
        
        num_colors = len(colors.items())
        new_color = WebColors.get_random_value_array()
        inputs = [new_color]
        new_colors = None
        while new_colors is None:
            try:
                r = requests.post('http://colormind.io/api/', json={"input": inputs, "model": "ui"})
                if r.status_code != 200:
                    time.sleep(3) # Don't spam the API
                    print("No Color response")
                    continue
                else:
                    new_colors = [WebColors.as_string(color, withAlpha=withAlpha) for color in r.json()['result']]
            except:
                time.sleep(3)
                continue
        # Assign each color to a new color that is interesting
        i = random.randint(0,4)
        for color, newColor in colors.items():
            # print(f'Colors: {color}')
            n = i % 5
            colors[color] = new_colors[n]
            i += 1

        # TODO: Make them into variables or some way to mutate all of them at once (unify css colors)
        self.mutations = []
        for scope, selector, rule, color in website.css.background_colors():
            newcolor = colors[color]
            self.mutations.append(((scope, selector, rule, newcolor), []))

        # TODO: Add the concept of foreground & background contrast
        # Possible Ideas: 
        # * Always have foreground be Black and White & Background changes

class ColorSchemeFromAllImagesAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage, withAlpha:bool=False):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None
        
        num_colors = len(colors.items())
        new_colors = [WebColors.as_string(color, withAlpha=withAlpha) for color in generate_pallete_from_imgs()]
       
        # print(f"New Colors: {new_colors}")
        # Assign each color to a new color that is interesting
        i = random.randint(0,4)
        for color, newColor in colors.items():
            # print(f'Colors: {color}')
            n = i % 5
            colors[color] = new_colors[n]
            i += 1

        # TODO: Make them into variables or some way to mutate all of them at once (unify css colors)
        self.mutations = []
        for scope, selector, rule, color in website.css.background_colors():
            newcolor = colors[color]
            self.mutations.append(((scope, selector, rule, newcolor), []))

        # TODO: Add the concept of foreground & background contrast
        # Possible Ideas: 
        # * Always have foreground be Black and White & Background changes


class ColorSchemeFromImageAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage, withAlpha:bool=False):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None
        
        num_colors = len(colors.items())
        new_colors = [WebColors.as_string(color, withAlpha=withAlpha) for color in generate_pallete_from_random_img()]
        # print(f"num_colors: {len(new_colors)}")
        # Assign each color to a new color that is interesting
        i = random.randint(0,4)
        for color, newColor in colors.items():
            # print(f'Colors: {color}')
            n = i % 5
            colors[color] = new_colors[n]
            i += 1

        # TODO: Make them into variables or some way to mutate all of them at once (unify css colors)
        self.mutations = []
        for scope, selector, rule, color in website.css.background_colors():
            newcolor = colors[color]
            self.mutations.append(((scope, selector, rule, newcolor), []))

        # TODO: Add the concept of foreground & background contrast
        # Possible Ideas: 
        # * Always have foreground be Black and White & Background changes


class BrandArchetypeAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage, withAlpha:bool=False):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None

        num_colors = len(colors.items())
        new_color = archetypes.get_color(website.school_name)
        inputs = [new_color]
        new_colors = None
        while new_colors is None:
            try:
                r = requests.post('http://colormind.io/api/', json={"input": inputs, "model": "ui"})
                if r.status_code != 200:
                    time.sleep(3)  # Don't spam the API
                    print("No Color response")
                    continue
                else:
                    print(r.text)
                    new_colors = [WebColors.as_string(color, withAlpha=withAlpha) for color in r.json()['result']]
            except:
                time.sleep(3)
                continue
        # Assign each color to a new color that is interesting
        i = random.randint(0,4)
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
        newfont, link = archetypes.get_font_and_link(website.school_name)
        for scope, selector, rule, font in website.css.fonts():
            self.mutations.append(((scope, selector, rule, newfont), link))


class StrategicColorSchemeAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)
        # Get all of the colors in the page
        colors = {}
        for scope, selector, rule, color in website.css.background_colors():
            colors[color] = None

        num_colors = len(colors.items())
        # print(f'Website name: {website.school_name}')
        new_color = archetypes.get_color(website.school_name)
        inputs = [new_color]
        new_colors = None
        # print(inputs)
        while new_colors is None:
            try:
                r = requests.post('http://colormind.io/api/', json={"input": inputs, "model": "ui"})
                if r.status_code != 200:
                    time.sleep(3)  # Don't spam the API
                    print("No Color response")
                    continue
                else:
                    primary = r.json()['result'][0]
                    accent = r.json()['result'][1]
                    new_colors = [f"rgb({primary[0]},{primary[1]},{primary[2]})",
                                  f"rgb({accent[0]},{accent[1]},{accent[2]})",
                                  f"rgb({primary[0] // 2},{primary[1] // 2},{primary[2] // 2})",
                                  f"rgb({(primary[0] + 255) // 2},{(primary[1] + 255) // 2},{(primary[2] + 255) // 2})",
                                  "rgb(0,0,0)", "rgb(255,255,255)"]
            except:
                time.sleep(3)
                continue

        # Assign each color to a new color that is interesting
        for color, newColor in colors.items():
            colors[color] = random.choice(new_colors)

        self.mutations = []
        for scope, selector, rule, color in website.css.background_colors():
            newcolor = colors[color]
            self.mutations.append(((scope, selector, rule, newcolor), []))

class BlueEverythingAction(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)

        self.mutations = []
        for scope, selector, rule, _ in website.css.background_colors():
            self.mutations.append(((scope, selector, rule, "blue"), []))

def get_mutated_number(old_number):
    old_number = float(old_number.group())
    # If number is really small, don't mess with it.
    if abs(old_number) <= 1:
        return str(old_number)
    # If the number is kind of small, shift it a few units
    if abs(old_number) <= 8:
        return str(old_number + random.randint(-3, 3))
    return str(old_number * random.uniform(0.85, 1.15))


class MutatePageLayout(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)
        # Get all of the colors in the page
        self.mutations = []
        for scope, selector, rule, size in website.css.get_layout_sizes():
            new_size = re.sub('-?\\d+', get_mutated_number, size)
            self.mutations.append(((scope, selector, rule, new_size), []))


class MutateElementLayout(Action):
    def __init__(self, stats: GlobalStats, website: WebPage):
        super().__init__(stats, website)
        # Get all of the colors in the page
        self.mutations = []
        scope, selector, rule, size = random.choice(list(website.css.get_layout_sizes()))
        new_size = re.sub('-?\\d+', get_mutated_number, size)
        self.mutations.append(((scope, selector, rule, new_size), []))
