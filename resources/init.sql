create table if not exists rules (
    id integer not null primary key autoincrement,
    web_page text not null,
    selector text not null,
    rule_key text not null,
    rule_value text not null
);
CREATE INDEX RulesWebPageIndex ON rules(web_page);
CREATE INDEX RulesSelectorIndex ON rules(selector);
CREATE INDEX RulesRuleKeyIndex ON rules(rule_key);
CREATE INDEX RulesRuleValueIndex ON rules(rule_value);
CREATE INDEX RulesRuleKeyValueIndex ON rules(rule_key, rule_value);

create table if not exists tags (
    db_id integer not null primary key autoincrement,
    web_page text not null,
    name text not null,
    id text,
    classes text
);

CREATE INDEX TagsWebPageIndex ON tags(web_page);
CREATE INDEX TagsNameIndex ON tags(name);