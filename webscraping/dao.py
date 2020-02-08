import sqlite3
from typing import Tuple, List

class Rule:
    def __init__(self, id: int or None, web_page: str, selector: str, rule_key: str, rule_value: str):
        self.id, self.web_page, self.selector, self.rule_key, self.rule_value = id, web_page, selector, rule_key, rule_value

    def __str__(self):
        return f"Rule({self.id}, {self.web_page}, {self.selector}, {self.rule_key}, {self.rule_value})"

    def __repr__(self):
        return self.__str__()

# noinspection SqlResolve
class Dao:
    def __init__(self):
        """ create a database connection to a SQLite database """
        self.conn = sqlite3.connect("../resources/stats.sqlite")

    def add_rule(self, rule: Rule) -> Rule:
        new_id = self.execute("insert into rules (web_page, selector, rule_key, rule_value) values (?, ?, ?, ?)", (rule.web_page, rule.selector, rule.rule_key, rule.rule_value))
        rule.id = new_id
        return rule

    def add_rules(self, rules: [Rule]):
        self.execute_many("insert into rules (web_page, selector, rule_key, rule_value) values (?, ?, ?, ?)", [(rule.web_page, rule.selector, rule.rule_key, rule.rule_value) for rule in rules])

    # noinspection SqlWithoutWhere
    def flush_rules(self):
        cur = self.conn.cursor()
        cur.execute("delete from rules")

    def get_rules(self) -> [Rule]:
        return self.get_all(Rule, "select * from rules")

    # Utility functions

    def execute_many(self, sql: str, params: [Tuple]):
        cur = self.conn.cursor()
        cur.executemany(sql, params)
        self.conn.commit()

    def execute(self, sql: str, params: Tuple = None) -> int:
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur.lastrowid

    def get_all(self, klass, sql: str, params: Tuple = None) -> List:
        cur = self.conn.cursor()
        rows = cur.execute(sql).fetchall()
        return [klass(*row) for row in rows]
