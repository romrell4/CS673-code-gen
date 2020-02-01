from webscraping import web_scraper
import tinycss2
import json

def parse_website(url):
    soup = web_scraper.get_soup(url)
    css_stats = parse_styles(soup)
    tag_info = join_html_to_css(soup, css_stats)
    return tag_info

def parse_styles(html_soup):
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
        elif value.type == "number":
            return str(value.value)
        elif value.type == "string":
            return value.value
        elif value.type in ["whitespace", "literal"]:
            return value.value
        else:
            print("Unsupported value: {}".format(value))
            return ""

    styles = html_soup.find_all("style")
    stats = {"tags": {}, "ids": {}, "classes": {}}
    for style in styles:
        css = tinycss2.parse_stylesheet(style.text)
        for rule_set in css:
            if rule_set.type == "qualified-rule":
                prelude = [token for token in rule_set.prelude if token.type != "whitespace"]
                if len(prelude) == 1:
                    subject = prelude[0]
                    if subject.type == "ident":
                        stats["tags"][subject.lower_value] = parse_declarations(rule_set)
                    elif subject.type == "hash":
                        stats["ids"][subject.value] = parse_declarations(rule_set)
                    else:
                        # TODO: Support other types?
                        print("Unsupported prelude type: {}".format(subject.type))
                elif len(prelude) == 2:
                    if prelude[0].type == "literal" and prelude[0].value == "." and prelude[1].type == "ident":
                        stats["classes"][prelude[1].lower_value] = parse_declarations(rule_set)
                else:
                    # TODO: Support other cases?
                    print("Unsupported prelude size '{}': {}".format(len(prelude), prelude))
    # print(json.dumps(stats, indent = 2))
    return stats

def join_html_to_css(html_soup, css_stats):
    tags = web_scraper.parse_children(html_soup.body)
    tag_info = {}
    for tag in set(tags):
        if tag.name not in tag_info:
            tag_info[tag.name] = {}
        tag_info[tag.name].update(css_stats["tags"].get(tag.name, {}))
        [tag_info[tag.name].update(css_stats["classes"].get(klass, {})) for klass in tag.classes]
        tag_info[tag.name].update(css_stats["ids"].get(tag.id, {}))
    return tag_info


if __name__ == '__main__':
    tag_info = parse_website("combined.html")
    print(json.dumps(tag_info, indent = 2))
