from webscraping import web_scraper
import tinycss2
import json

def get_css_stats(url):
    stats = {
        "tags": {},
        "ids": {},
        "classes": {}
    }

    def parse_rule_set(rule):
        if rule.type == "qualified-rule":
            prelude = [token for token in rule.prelude if token.type != "whitespace"]
            if len(prelude) == 1:
                subject = prelude[0]
                if subject.type == "ident":
                    stats["tags"][subject.lower_value] = parse_declarations(rule)
                elif subject.type == "hash":
                    stats["ids"][subject.value] = parse_declarations(rule)
                else:
                    # TODO: Support other types?
                    print("Unsupported prelude type: {}".format(subject.type))
            elif len(prelude) == 2:
                if prelude[0].type == "literal" and prelude[1].type == "ident":
                    stats["classes"][prelude[1].lower_value] = parse_declarations(rule)
            else:
                # TODO: Support other cases?
                print("Unsupported prelude size '{}': {}".format(len(prelude), prelude))

    def parse_declarations(rule):
        declarations = tinycss2.parse_declaration_list(rule.content, skip_comments = True, skip_whitespace = True)

        dec_dict = {}
        for declaration in declarations:
            values = declaration.value
            dec_dict[declaration.lower_name] = "".join([parse_value(value) for value in values]).strip()

        return dec_dict

    def parse_value(value):
        if value.type == "percentage":
            return "{}%".format(value.value)
        elif value.type == "dimension":
            return "{}{}".format(value.value, value.unit)
        elif value.type == "url":
            return "url({})".format(value.value)
        elif value.type == "ident":
            return value.value
        elif value.type == "hash":
            return "#{}".format(value.value)
        elif value.type in ["whitespace", "literal"]:
            return value.value
        else:
            print("Unsupported value: {}".format(value))
            return value.value

    soup = web_scraper.scrape(url)
    styles = soup.find_all("style")
    for style in styles:
        css = tinycss2.parse_stylesheet(style.text)
        for rule_set in css:
            parse_rule_set(rule_set)

    print(json.dumps(stats, indent = 2))


if __name__ == '__main__':
    get_css_stats("test.html")