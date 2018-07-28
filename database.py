"""
This module work with databases on sqlite.

Created on 17.02.2018

@author: Ruslan Dolovanyuk

"""

import sqlite3


class Database:
    """The class for work databases on sqlite."""

    def __init__(self):
        """Initialize class for control databases."""
        self.conn = None
        self.cursor = None

    def connect(self, file_name):
        """Connect database."""
        self.conn = sqlite3.connect(file_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Disconnect database."""
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def get(self, script):
        """Get data from database."""
        self.cursor.execute(script)
        return self.cursor.fetchall()

    def put(self, script):
        """Set data in database."""
        if isinstance(script, str):
            self.cursor.execute(script)
        else:
            for line in script:
                self.cursor.execute(line)
        self.conn.commit()

    def if_exists(self, table):
        """Check table if exist in database."""
        str_sql = 'SELECT * FROM sqlite_master WHERE name = "%s"' % table
        self.cursor.execute(str_sql)
        if self.cursor.fetchone():
            return True
        return False

    def get_tables_names(self):
        """Return list tables names from database."""
        str_sql = 'SELECT name FROM sqlite_master WHERE type = "table"'
        self.cursor.execute(str_sql)
        return self.cursor.fetchall()

    def get_table_params(self, name):
        """Return list params table from database."""
        str_sql = 'PRAGMA TABLE_INFO(%s)' % name
        self.cursor.execute(str_sql)
        return self.cursor.fetchall()

    def dump(self, file_sql):
        """Dump database in sql file."""
        with open(file_sql, 'w', encoding='utf-8') as sql:
            for line in self.conn.iterdump():
                sql.write('%s\n' % line)

    def restore(self, file_sql):
        """Restore database from sql file."""
        with open(file_sql, 'r') as sql:
            for line in sql:
                self.cursor.execute(line)
