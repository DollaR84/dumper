"""
Creating dumps sqlite database for import mysql.

Created on 18.02.2018

@author: Ruslan Dolovanyuk

"""

import os

from database import Database


class Dumper:
    """Class for creating sqlite database."""

    def __init__(self):
        """Initialize dumper class."""
        self.db_name = None
        self.__db = Database()

        self.param_types = ['TEXT', 'INTEGER']

    def start(self, database_name):
        """Connect database."""
        name = os.path.splitext(database_name)[0]
        self.db_name = name.split('/')[-1]
        self.__db.connect(database_name)

    def finish(self):
        """Close database connection."""
        self.__db.disconnect()

    def add_table(self, name, params):
        """Add table in database."""
        scripts = []
        script = 'DROP TABLE IF EXISTS %s' % name
        scripts.append(script)
        script = 'CREATE TABLE %s (id INTEGER NOT NULL PRIMARY KEY, ' % name
        for param in params:
            script += param
            if param != params[-1]:
                script += ', '
        script += ') WITHOUT ROWID'
        scripts.append(script)
        self.__db.put(scripts)

    def get_tables_names(self):
        """Return list tables names from database."""
        return [row[0] for row in self.__db.get_tables_names()]

    def get_param_types(self):
        """Return list param types."""
        return self.param_types

    def get_table_params(self, name):
        """Return list params name and type table from database."""
        params = self.__db.get_table_params(name)
        return [(row[1], row[2], row[3], row[4]) for row in params if 1 != row[5]]

    def get_table_rows(self, name):
        """Return all rows in table."""
        script = 'SELECT * FROM %s' % name
        return self.__db.get(script)

    def get_table_last_id(self, name):
        """Return last id primary key."""
        script = 'SELECT id FROM %s ORDER BY id DESC LIMIT 1' % name
        last = self.__db.get(script)
        if last:
            return last[0][0]
        return 0

    def get_table_cell(self, table, index, param):
        """Return value column in row table."""
        script = 'SELECT %s FROM %s WHERE id=%d' % (param, table, index)
        result = self.__db.get(script)
        return result[0][0]

    def insert(self, table, values_types):
        """Add new row in table."""
        params = self.get_table_params(table)
        index = self.get_table_last_id(table) + 1
        script = 'INSERT INTO %s (id, ' % table
        idx = 1
        for param in params:
            script += param[0]
            if idx < len(params):
                script += ', '
            idx += 1
        script += ') VALUES (%d, ' % index
        idx = 1
        for value, typ in values_types:
            if 'TEXT' == typ:
                script += '"%s"' % value
            elif 'INTEGER' == typ:
                script += '%d' % value
            if idx < len(values_types):
                script += ', '
            idx += 1
        script += ')'
        self.__db.put(script)

    def update(self, table, index, param, value_type):
        """Update one param in table."""
        script = 'UPDATE %s SET %s=' % (table, param)
        if 'TEXT' == value_type[1]:
            script += '"%s"' % value_type[0]
        elif 'INTEGER' == value_type[1]:
            script += '%d' % value_type[0]
        script += ' WHERE id=%d' % index
        self.__db.put(script)

    def delete(self, table, index):
        """Delete row in table."""
        script = 'DELETE FROM %s WHERE id=%d' % (table, index)
        self.__db.put(script)
        last = self.get_table_last_id(table)
        idx = index + 1
        while idx <= last:
            self.update(table, idx, 'id', (idx-1, 'INTEGER'))
            idx += 1

    def dump(self, file_name):
        """Create dump file sql."""
        self.__db.dump(file_name)

    def __read(self, file_name):
        """Return content dump sql file."""
        with open(file_name, 'r') as file_sql:
            return file_sql.read()

    def __write(self, file_name, content):
        """Write file dump sql."""
        with open(file_name, 'w') as file_sql:
            file_sql.write(content)

    def fix_quote(self, text):
        """Fix quote in text."""
        return text.replace('"', '""')

    def fix_amp(self, text):
        """Fix amp for html."""
        idx = text.find('&')
        while -1 != idx:
            if ((('&amp;' != text[idx:idx+4]) or
                 ('&lt;' != text[idx:idx+3]) or
                 ('&gt;' != text[idx:idx+3]) or
                 ('&quot;' != text[idx:idx+5]) or
                 ('&nbsp;' != text[idx:idx+5]))):
                text = text[:idx] + '&amp;' + text[idx+1:]
            idx = text.find('&', idx+1)
        return text

    def fix_html(self, text):
        """Fix text for correct view in html."""
        result = self.fix_amp(text)
        result = result.replace('<', '&lt;')
        result = result.replace('>', '&gt;')
        result = result.replace('"', '&quot;')
        return result.replace('\n', '<br>\n')

    def fix_mysql(self, file_name):
        """Fix dump file sqlite for mysql database."""
        content = self.__read(file_name)
        content = content.replace('BEGIN TRANSACTION;', 'START TRANSACTION;')
        content = content.replace('PRIMARY KEY', 'PRIMARY KEY AUTO_INCREMENT')
        content = content.replace(' WITHOUT ROWID;', ';')
        self.__write(file_name, content)

    def add_drop_tables(self, file_name):
        """Add row drop table."""
        content = self.__read(file_name)
        create_str = 'CREATE TABLE '
        drop_str = 'DROP TABLE IF EXISTS '

        index = content.find(create_str)
        while -1 != index:
            idx2space = content.find(' ', index+len(create_str)+1)
            name = content[index+len(create_str):idx2space] + ';\n'
            result = content[:index] + drop_str + name
            result += content[index:]
            content = result
            start_index = index + len(drop_str) + len(name) + len(create_str) + 1
            index = content.find(create_str, start_index)
        self.__write(file_name, content)

    def add_database_name(self, file_name):
        """Add database name."""
        content = self.__read(file_name)
        strs = [
                'CREATE TABLE ',
                'DROP TABLE IF EXISTS ',
                'INSERT INTO ',
                'UPDATE '
               ]

        for cur_str in strs:
            index = content.find(cur_str)
            while -1 != index:
                idx = index + len(cur_str)
                result = content[:idx] + self.db_name + '.' + content[idx:]
                content = result
                index = content.find(cur_str, idx)
        self.__write(file_name, content)

    def del_quotes_around_table_name(self, file_name):
        """Remove quotes around table name."""
        content = self.__read(file_name)
        strs = [
                'INSERT INTO ',
                'UPDATE '
               ]

        for cur_str in strs:
            result = content
            index = content.find(cur_str)
            while -1 != index:
                idx = index + len(cur_str)
                if '"' == content[idx]:
                    i2s = content.find(' ', idx)
                    result = content[:idx] + content[idx+1:i2s-1] + content[i2s:]
                    content = result
                index = content.find(cur_str, idx)
        self.__write(file_name, content)
