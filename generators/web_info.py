import random
import os
import json

class WebColors:
    rules = ['background-color', 'color']
    def __init__(self):
        pass

    @staticmethod
    def get_random_rule() -> str:
        return random.choice(WebColors.rules)

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
        with open(os.path.join('../', 'resources', 'fonts.json')) as file:
            fonts = json.load(file)
            for item in fonts['items']:
                if ' ' in item['family']:
                    print(f"\"{item['family']}\"")
                else:
                    print(item['family'])

    @staticmethod
    def get_random_rule() -> str:
        return random.choices(WebFonts.rules, WebFonts.rule_probs)[0]

    @staticmethod
    def get_random_value(rule: str) -> str:
        return random.choice(WebFonts.rule_values[rule])


webFonts = WebFonts()