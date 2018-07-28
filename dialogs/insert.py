"""
Dialog insert row in database.

Created on 04.04.2018

@author: Ruslan Dolovanyuk

"""

import string

from dialogs.dialogs import Message

import wx


class InsertDialog(wx.Dialog):
    """Create interface dialog insert row."""

    def __init__(self, parent):
        """Initialize interface."""
        super().__init__(parent, wx.ID_ANY, 'Вставка записи')
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.command = parent.command
        self.message = Message(self)
        index = parent.tables.GetSelection()
        self.table = self.command.dumper.get_tables_names()[index]
        self.params = self.command.dumper.get_table_params(self.table)
        self.values = [param[3] for param in self.params]
        self.names = [param[0] for param in self.params]

        box_columns = wx.StaticBox(self, wx.ID_ANY, 'Столбцы')
        self.columns = wx.ListBox(self, wx.ID_ANY, choices=self.names,
                                  style=wx.LB_SINGLE | wx.LB_HSCROLL,
                                  validator=NotNullValidator())
        self.value = wx.TextCtrl(self, wx.ID_ANY,
                                 style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER,
                                 validator=NumberValidator())
        label = 'Заменить && на html код'
        self.fix_amp = wx.CheckBox(self, wx.ID_ANY, label)
        label = 'Заменить символы (&&, <, >, ", \\n) на html коды'
        self.fix_html = wx.CheckBox(self, wx.ID_ANY, label)
        but_set = wx.Button(self, wx.ID_ANY, 'Задать')
        but_save = wx.Button(self, wx.ID_OK, 'Сохранить')
        but_cancel = wx.Button(self, wx.ID_CANCEL, 'Отмена')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_panels = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_left = wx.StaticBoxSizer(box_columns, wx.VERTICAL)
        sizer_left.Add(self.columns, 1, wx.EXPAND | wx.ALL, 5)
        sizer_panels.Add(sizer_left, 1, wx.EXPAND | wx.ALL)
        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(self.value, 1, wx.EXPAND | wx.ALL, 5)
        sizer_right.Add(self.fix_amp, 0, wx.EXPAND | wx.ALL, 5)
        sizer_right.Add(self.fix_html, 0, wx.EXPAND | wx.ALL, 5)
        sizer_right.Add(but_set, 0, wx.ALIGN_CENTER, 5)
        sizer_panels.Add(sizer_right, 1, wx.EXPAND | wx.ALL)
        sizer.Add(sizer_panels, 1, wx.EXPAND | wx.ALL)
        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_save, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LISTBOX, self.select_column, self.columns)
        self.Bind(wx.EVT_BUTTON, self.set_column, but_set)

        self.fix_amp.SetValue(False)
        self.fix_html.SetValue(False)
        but_save.SetDefault()
        self.Layout()

    def select_column(self, event):
        """Change selection in columns listbox."""
        index = self.columns.GetSelection()
        if self.values[index] is not None:
            if 'TEXT' == self.params[index][1]:
                self.value.SetValue(self.values[index])
            else:
                self.value.SetValue(str(self.values[index]))
        else:
            self.value.SetValue('')
        self.Layout()

    def set_column(self, event):
        """Set column in database."""
        index = self.columns.GetSelection()
        if 'TEXT' == self.params[index][1]:
            text = self.value.GetValue()
            flag = self.fix_amp.GetValue()
            text = self.command.dumper.fix_amp(text) if flag else text
            flag = self.fix_html.GetValue()
            text = self.command.dumper.fix_html(text) if flag else text
            text = self.command.dumper.fix_quote(text) if not flag else text
            self.values[index] = text
        elif 'INTEGER' == self.params[index][1]:
            value = self.value.GetValue()
            self.values[index] = int(value) if '' != value else 0


class NotNullValidator(wx.Validator):
    """Validate empty values."""

    def __init__(self):
        """Initialize validator."""
        super().__init__()

    def Clone(self):
        """Be sure function."""
        return NotNullValidator()

    def Validate(self, win):
        """Check method for validator."""
        for index, value in enumerate(win.values):
            if (value is None) and (1 == win.params[index][2]):
                mes = 'Не задано обязательное поле: ' + win.params[index][0]
                win.message.error('Ошибка NOT NULL', mes)
                return False
        return True

    def TransferToWindow(self):
        """Check values loading to window."""
        return True

    def TransferFromWindow(self):
        """Check values loading from window."""
        return True


class NumberValidator(wx.Validator):
    """Validate number values for INTEGER column."""

    def __init__(self):
        """Initialize validator."""
        super().__init__()
        rus_low = set('аоуыэяеёюибвгдйжзклмнпрстфхцчшщьъ')
        rus_up = set('АОУЫЭЯЕЁЮИБВГДЙЖЗКЛМНПРСТФХЦЧШЩЬЪ')
        symbols = set('!?:;"., ')
        self.all = set().union(string.ascii_letters, symbols, rus_low, rus_up)

        self.Bind(wx.EVT_CHAR, self.check_char)

    def Clone(self):
        """Be sure function."""
        return NumberValidator()

    def Validate(self, win):
        """Check method for validator."""
        return True

    def TransferToWindow(self):
        """Check values loading to window."""
        return True

    def TransferFromWindow(self):
        """Check values loading from window."""
        return True

    def check_char(self, event):
        """Check number value if INTEGER column."""
        dlg = event.GetEventObject().GetParent()
        index = dlg.columns.GetSelection()
        if 'INTEGER' == dlg.params[index][1]:
            key = chr(event.GetUnicodeKey())
            if key in self.all:
                return
        event.Skip()
