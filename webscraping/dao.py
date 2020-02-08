import sqlite3
from typing import Tuple, List, Dict, Iterable

class Rule:
    def __init__(self, id: int or None, web_page: str, selector: str, rule_key: str, rule_value: str):
        self.id, self.web_page, self.selector, self.rule_key, self.rule_value = id, web_page, selector, rule_key, rule_value

    def __str__(self):
        return f"Rule({self.id}, {self.web_page}, {self.selector}, {self.rule_key}, {self.rule_value})"

    def __repr__(self):
        return self.__str__()

class ValueCount:
    def __init__(self, value, count: int):
        self.value, self.count = value, count

    def __str__(self):
        return f"ValueCount({self.value}, {self.count})"

    def __repr__(self):
        return self.__str__()

# noinspection SqlResolve
class Dao:
    def __init__(self):
        """ create a database connection to a SQLite database """
        self.conn = sqlite3.connect("../resources/stats.sqlite")

    # Used by stat generator

    def add_rules(self, rules: [Rule]):
        self.execute_many("insert into rules (web_page, selector, rule_key, rule_value) values (?, ?, ?, ?)", [(rule.web_page, rule.selector, rule.rule_key, rule.rule_value) for rule in rules])

    # noinspection SqlWithoutWhere
    def flush_rules(self):
        cur = self.conn.cursor()
        cur.execute("delete from rules")

    # Used for actual stat model

    def get_rule_key_counts(self, website: str or None = None, selector: str or None = None) -> [ValueCount]:
        sql = "select rule_key, count(*) from rules where true"
        params = []
        if website is not None:
            sql += " and website = ?"
            params += website
        if selector is not None:
            sql += " and selector = ?"
            params += selector
        sql += " group by rule_key order by rule_key"
        return self.get_all(ValueCount, sql, params)

    def get_rule_values_by_rule_key(self) -> Dict[str, List[ValueCount]]:
        sql = "select rule_key, rule_value, count(*) as count from rules group by rule_key, rule_value order by rule_key, count"
        result = {}
        for key, value, count in self.get_all(None, sql):
            if key not in result:
                result[key] = []
            result[key].append(ValueCount(value, count))
        return result

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

    def get_all(self, klass, sql: str, params: Iterable = ()) -> List:
        cur = self.conn.cursor()
        rows = cur.execute(sql, params).fetchall()
        if klass is not None:
            return [klass(*row) for row in rows]
        else:
            return rows


if __name__ == '__main__':
    print(Dao().get_rule_values_by_rule_key())