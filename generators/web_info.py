import random
import os
import json
import csv
from typing import Dict


class WebColors:
    rules = ['background-color', 'color']
    def __init__(self):
        pass

    @staticmethod
    def get_random_rule() -> str:
        return random.choice(WebColors.rules)

    @staticmethod
    def get_random_value_array() -> str:
        r = random.randint(0, 25)*10
        g = random.randint(0, 25)*10
        b = random.randint(0, 25)*10
        a = abs(random.random())
        return [r,g,b]

    @staticmethod
    def get_random_value() -> str:
        r = random.randint(0, 25)*10
        g = random.randint(0, 25)*10
        b = random.randint(0, 25)*10
        a = abs(random.random())
        return f"rgb({r},{g},{b})"



class WebFonts:
    rules = ["font-family", 'font-size', 'font-style', 'font-weight', 'font-variant']
    rule_probs = [.35, .35, .15, .1, .05]
    rule_values = {'font-family': ['"Times New Roman"', 'Times', 'serif', 'sans-serif', 'Arial', 'Verdana', '"Courier New"', 'Georgia', 'Lucida Console'],
                    'font-size': ['18px', '14px', '38px', '24px', '14px', '30px', '1.8em', '.9em', '1.2em', '1.5em'],
                    'font-style': ['normal', 'italic', 'oblique'],
                    'font-weight': ['normal', 'bold'],
                    'font-variant': ['normal', 'small-caps']}

    

    def __init__(self):
        self.fonts = {}
        with open(os.path.join('../', 'resources', 'fonts.json')) as file:
            fonts = json.load(file)
            count = 0
            for item in fonts['items']:
                if ' ' in item['family']:
                    item['family'] = f"\"{item['family']}\""
                if 'latin' in item['subsets']:
                    count += 1
                    # print(item['family'] + str(count))
                    # print(self.link_tag(item['family']))
                    self.fonts[item['family']] = self.link_tag(item['family'])
        # print(self.fonts)
        self.rule_values['font-family'] = list(self.fonts.keys())
        self.rule_values['font-family'].extend(['serif', 'sans-serif'])

    @staticmethod
    def link_tag(family:str) -> str:
        familyFormatted = family.replace(' ', '%20').replace('"','')
        return [f'https://fonts.googleapis.com/css?family={familyFormatted}',f'https://fonts.googleapis.com/css?family={familyFormatted}:bold',f'https://fonts.googleapis.com/css?family={familyFormatted}:italic']            

    @staticmethod
    def get_random_rule() -> str:
        return random.choices(WebFonts.rules, WebFonts.rule_probs)[0]

    @staticmethod
    def get_random_value(rule: str) -> str:
        return random.choice(WebFonts.rule_values[rule])

    def get_rule_links(self, font: str)-> str:
        return self.fonts.get(font, None)


webFonts = WebFonts()


class Archetypes:
    def __init__(self):
        self.websites: Dict[str, str] = {}
        with open(os.path.join('../', 'resources', 'website_archetypes.csv')) as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                self.websites[line[0]] = line[1]
        
        self.archetypes = {}
        with open(os.path.join('../', 'resources', 'archetype_schemes.json')) as json_file:
            for item in json.load(json_file)['archetypes']:
                self.archetypes[item['name']] = item
    
    def get_font(self, school):
        archetype = self.websites[school]
        features = self.archetypes[archetype]
        return features['font-groups'][0]

    def get_color(self, school):
        archetype = self.websites[school]
        features = self.archetypes[archetype]
        hexcolor = features['colorschemes'][0]
        r = int(hexcolor[1:3], 16)
        g = int(hexcolor[3:5], 16)
        b = int(hexcolor[5:7], 16)
        return [r, g, b]


archetypes = Archetypes()