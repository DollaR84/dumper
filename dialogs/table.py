"""
Module contains description table for Grid komponent.

Created on 07.04.2018

@author: Ruslan Dolovanyuk

"""

import wx.grid


class Table(wx.grid.GridTableBase):
    """Class table for link grid and db."""

    def __init__(self, dumper, table):
        """Initialize table."""
        super().__init__()
        self.dumper = dumper
        self.table = table
        self.params = self.dumper.get_table_params(self.table)
        self.buffer = []

    def GetNumberRows(self):
        """Return count rows in table."""
        return self.dumper.get_table_last_id(self.table)

    def GetNumberCols(self):
        """Return count cols in table."""
        return len(self.params)

    def IsEmptyCell(self, row, col):
        """Return state cell in data table."""
        param = self.params[col][0]
        value = self.dumper.get_table_cell(self.table, row+1, param)
        return value is not None

    def GetValue(self, row, col):
        """Return value cell from data table."""
        param = self.params[col][0]
        value = self.dumper.get_table_cell(self.table, row+1, param)
        if value is not None:
            if 'TEXT' == self.params[col][1]:
                return value
            elif 'INTEGER' == self.params[col][1]:
                return str(value)
        else:
            return ''

    def SetValue(self, row, col, value):
        """Set value cell in data table."""
        self.buffer.append((row, col, self.GetValue(row, col)))
        self.__update_cell_db(row, col, value)

    def GetRowLabelValue(self, row):
        """Return row label."""
        return str(row+1)

    def GetColLabelValue(self, col):
        """Return col label."""
        return self.params[col][0]

    def DeleteRows(self, pos=0, numRows=1):
        """Delete row from database."""
        self.dumper.delete(self.table, pos+1)
        return True

    def cancel_update_db(self):
        """Cancel update database from buffer."""
        for row, col, value in self.buffer:
            self.__update_cell_db(row, col, value)

    def __update_cell_db(self, row, col, value):
        """Set value in database."""
        value_type = ()
        types = self.params[col][1]
        if 'TEXT' == types:
            value_type = (value, types)
        elif 'INTEGER' == types:
            value_type = (int(value), types)
        self.dumper.update(self.table, row+1, self.params[col][0], value_type)
