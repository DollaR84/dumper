"""
Dialog update row in database.

Created on 10.04.2018

@author: Ruslan Dolovanyuk

"""

from dialogs.table import Table

import wx
import wx.grid


class UpdateDialog(wx.Dialog):
    """Create interface dialog update row."""

    def __init__(self, parent):
        """Initialize interface."""
        super().__init__(parent, wx.ID_ANY, 'Изменение записи')
        self.command = parent.command
        index = parent.tables.GetSelection()
        table_name = self.command.dumper.get_tables_names()[index]
        self.table = Table(self.command.dumper, table_name)

        self.grid = wx.grid.Grid(self, wx.ID_ANY)
        self.grid.SetTable(self.table, True)
        for col, param in enumerate(self.table.params):
            if 'INTEGER' == param[1]:
                self.grid.SetColFormatNumber(col)
                row = 0
                while row < self.table.GetNumberRows():
                    editor = wx.grid.GridCellNumberEditor()
                    self.grid.SetCellEditor(row, col, editor)
                    row += 1
        but_update = wx.Button(self, wx.ID_OK, 'Изменить')
        but_cancel = wx.Button(self, wx.ID_CANCEL, 'Отмена')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_update, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
