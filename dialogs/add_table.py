"""
Dialog add table.

Created on 04.04.2018

@author: Ruslan Dolovanyuk

"""

from dialogs.dialogs import Message

import wx


class AddTableDialog(wx.Dialog):
    """Create interface dialog add table."""

    def __init__(self, parent):
        """Initialize interface."""
        super().__init__(parent, wx.ID_ANY, 'Добавление таблицы')
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.command = parent.command
        self.message = Message(self)
        self.params = []
        self.param_names = []

        box_table = wx.StaticBox(self, wx.ID_ANY, 'Наименование таблицы')
        self.table = wx.TextCtrl(self, wx.ID_ANY, validator=TableValidator())
        box_columns = wx.StaticBox(self, wx.ID_ANY, 'Столбцы')
        box_name = wx.StaticBox(box_columns, wx.ID_ANY, 'Имя')
        self.name = wx.TextCtrl(box_name, wx.ID_ANY)
        box_type = wx.StaticBox(box_columns, wx.ID_ANY, 'Тип')
        self.type = wx.Choice(box_type, wx.ID_ANY,
                              choices=parent.command.dumper.get_param_types())
        self.not_null = wx.CheckBox(box_columns, wx.ID_ANY, 'NOT NULL')
        but_add = wx.Button(box_columns, wx.ID_ANY, 'Добавить')
        self.columns = wx.ListBox(self, wx.ID_ANY, choices=self.param_names,
                                  style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.but_del = wx.Button(self, wx.ID_ANY, 'Удалить')
        but_save = wx.Button(self, wx.ID_OK, 'Сохранить')
        but_cancel = wx.Button(self, wx.ID_CANCEL, 'Отмена')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_panels = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_table = wx.StaticBoxSizer(box_table, wx.HORIZONTAL)
        sizer_table.Add(self.table, 1, wx.EXPAND | wx.ALL, 5)
        sizer_left.Add(sizer_table, 0, wx.EXPAND | wx.ALL)
        sizer_columns = wx.StaticBoxSizer(box_columns, wx.VERTICAL)
        sizer_name = wx.StaticBoxSizer(box_name, wx.HORIZONTAL)
        sizer_name.Add(self.name, 1, wx.EXPAND | wx.ALL, 5)
        sizer_columns.Add(sizer_name, 0, wx.EXPAND | wx.ALL)
        sizer_type = wx.StaticBoxSizer(box_type, wx.HORIZONTAL)
        sizer_type.Add(self.type, 1, wx.EXPAND | wx.ALL, 5)
        sizer_columns.Add(sizer_type, 0, wx.EXPAND | wx.ALL)
        sizer_columns.Add(self.not_null, 0, wx.EXPAND | wx.ALL, 5)
        sizer_columns.Add(but_add, 0, wx.ALIGN_CENTER, 5)
        sizer_left.Add(sizer_columns, 1, wx.EXPAND | wx.ALL)
        sizer_panels.Add(sizer_left, 1, wx.EXPAND | wx.ALL)
        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(self.columns, 1, wx.EXPAND | wx.ALL, 5)
        sizer_right.Add(self.but_del, 0, wx.ALIGN_CENTER, 5)
        sizer_panels.Add(sizer_right, 1, wx.EXPAND | wx.ALL)
        sizer.Add(sizer_panels, 1, wx.EXPAND | wx.ALL)
        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_save, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.add_column, but_add)
        self.Bind(wx.EVT_BUTTON, self.del_column, self.but_del)
        self.Bind(wx.EVT_LISTBOX, self.sel_column, self.columns)

        but_save.SetDefault()
        self.not_null.SetValue(True)
        self.type.SetSelection(0)
        self.but_del.Disable()
        self.Layout()

    def add_column(self, event):
        """Add column in list params."""
        typ = self.command.dumper.get_param_types()[self.type.GetSelection()]
        name = self.name.GetValue()
        if '' == name:
            self.message.error('Ошибка имени столбца',
                               'Имя столбца не указано')
        elif name in self.param_names:
            self.message.error('Ошибка имени столбца',
                               'Данное имя уже существует')
        elif 'id' == name:
            self.message.error('Ошибка имени столбца',
                               'Данное имя зарезервировано')
        else:
            not_null = ' NOT NULL' if self.not_null.GetValue() else ''
            param = name + ' ' + typ + not_null
            self.params.append(param)
            self.param_names.append(name)
            self.columns.Set(self.param_names)
            self.name.SetValue('')
            self.type.SetSelection(0)
            self.not_null.SetValue(True)
            self.Layout()

    def sel_column(self, event):
        """Change selection in columns list."""
        self.but_del.Enable()

    def del_column(self, event):
        """Delete column from list."""
        index = self.columns.GetSelection()
        self.param_names.pop(index)
        self.columns.Set(self.param_names)
        self.but_del.Disable()
        self.Layout()


class TableValidator(wx.Validator):
    """Validate table text control on empty value or clone name uses tables."""

    def __init__(self):
        """Initialize validator."""
        super().__init__()

    def Clone(self):
        """Be sure function."""
        return TableValidator()

    def Validate(self, win):
        """Check method for validator."""
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        if 0 == len(text):
            win.message.error('Ошибка', 'Наименование таблицы не указано')
            text_ctrl.SetFocus()
            return False
        else:
            tables = win.command.dumper.get_tables_names()
            if text in tables:
                win.message.error('Ошибка',
                                  'Таблица с таким именем уже существует')
                text_ctrl.SetFocus()
                return False
            return True

    def TransferToWindow(self):
        """Check values loading to window."""
        return True

    def TransferFromWindow(self):
        """Check values loading from window."""
        return True
