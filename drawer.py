"""
Graphical form for Dumper.

Created on 16.03.2018

@author: Ruslan Dolovanyuk

"""

from commands import Commands

from dialogs.add_table import AddTableDialog
from dialogs.delete import DeleteDialog
from dialogs.insert import InsertDialog
from dialogs.update import UpdateDialog

import wx


class Drawer:
    """Main class graphical form for Dumper."""

    def __init__(self, dumper):
        """Initilizing drawer form."""
        self.app = wx.App()
        self.wnd = DumperFrame(dumper)
        self.wnd.Show(True)
        self.app.SetTopWindow(self.wnd)

    def mainloop(self):
        """Graphical main loop running."""
        self.app.MainLoop()


class DumperFrame(wx.Frame):
    """Create user interface."""

    def __init__(self, dumper):
        """Initialize interface."""
        super().__init__(None, wx.ID_ANY, 'Конструктор дампов базы данных')
        self.command = Commands(self, dumper)
        self.path = ''
        title_db = 'Выбор базы SQLITE:'
        wildcard_db = 'sqlite database file (*.db)|*.db|' \
                      'All files (*.*)|*.*'
        self.path_sql = ''
        title_sql = 'Выбор файла дампа:'
        wildcard_sql = 'SQL dump file (*.sql)|*.sql|' \
                       'All files (*.*)|*.*'

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        box_db_browse = wx.StaticBox(panel, wx.ID_ANY, 'База Данных')
        self.db_ctrl = wx.FilePickerCtrl(box_db_browse,
                                         wx.ID_ANY,
                                         self.path,
                                         title_db,
                                         wildcard_db,
                                         style=wx.FLP_OPEN |
                                         wx.FLP_USE_TEXTCTRL)
        self.db_ctrl.GetPickerCtrl().SetLabel('Обзор...')
        self.but_connect = wx.ToggleButton(panel, wx.ID_ANY, 'Подключить')
        box_tables = wx.StaticBox(panel, wx.ID_ANY, 'Таблицы')
        self.but_add_table = wx.Button(box_tables, wx.ID_ANY, 'Добавить')
        self.tables = wx.Choice(box_tables, wx.ID_ANY, choices=[])
        box_rows = wx.StaticBox(panel, wx.ID_ANY, 'Записи')
        self.but_insert = wx.Button(box_rows, wx.ID_ANY, 'Вставить')
        self.but_update = wx.Button(box_rows, wx.ID_ANY, 'Обновить')
        self.but_delete = wx.Button(box_rows, wx.ID_ANY, 'Удалить')
        box_fix = wx.StaticBox(panel, wx.ID_ANY, 'Корректировки')
        self.mysql = wx.CheckBox(box_fix, wx.ID_ANY, 'Служебные правки')
        self.drop_table = wx.CheckBox(box_fix, wx.ID_ANY,
                                      'Добавить строку удаления таблицы')
        self.del_quotes = wx.CheckBox(box_fix, wx.ID_ANY,
                                      'Удалить кавычки вокруг имени таблицы')
        self.add_db = wx.CheckBox(box_fix, wx.ID_ANY,
                                  'Добавить имя БД перед именем таблицы')
        box_sql_browse = wx.StaticBox(panel, wx.ID_ANY, 'Файл дампа')
        self.sql_ctrl = wx.FilePickerCtrl(box_sql_browse,
                                          wx.ID_ANY,
                                          self.path_sql,
                                          title_sql,
                                          wildcard_sql,
                                          style=wx.FLP_SAVE |
                                          wx.FLP_USE_TEXTCTRL)
        self.sql_ctrl.GetPickerCtrl().SetLabel('Обзор...')
        self.but_save = wx.Button(panel, wx.ID_ANY, 'Сохранить')
        but_about = wx.Button(panel, wx.ID_ANY, 'О программе...')
        but_exit = wx.Button(panel, wx.ID_ANY, 'Выход')

        sizer = wx.BoxSizer(wx.VERTICAL)
        db_sizer = wx.BoxSizer(wx.HORIZONTAL)
        db_browse_sizer = wx.StaticBoxSizer(box_db_browse, wx.VERTICAL)
        db_browse_sizer.Add(self.db_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        db_sizer.Add(db_browse_sizer, 1, wx.EXPAND | wx.ALL, 5)
        db_sizer.Add(self.but_connect, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(db_sizer, 0, wx.EXPAND | wx.ALL)
        tables_sizer = wx.StaticBoxSizer(box_tables, wx.HORIZONTAL)
        tables_sizer.Add(self.but_add_table, 0, wx.EXPAND | wx.ALL, 5)
        tables_sizer.Add(self.tables, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(tables_sizer, 0, wx.EXPAND | wx.ALL)
        rows_sizer = wx.StaticBoxSizer(box_rows, wx.HORIZONTAL)
        rows_sizer.Add(self.but_insert, 0, wx.EXPAND | wx.CENTER, 5)
        rows_sizer.Add(self.but_update, 0, wx.EXPAND | wx.CENTER, 5)
        rows_sizer.Add(self.but_delete, 0, wx.EXPAND | wx.CENTER, 5)
        sizer.Add(rows_sizer, 0, wx.EXPAND | wx.ALL)
        fix_sizer = wx.StaticBoxSizer(box_fix, wx.VERTICAL)
        fix_sizer.Add(self.mysql, 0, wx.EXPAND | wx.ALL, 5)
        fix_sizer.Add(self.drop_table, 0, wx.EXPAND | wx.ALL, 5)
        fix_sizer.Add(self.del_quotes, 0, wx.EXPAND | wx.ALL, 5)
        fix_sizer.Add(self.add_db, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(fix_sizer, 1, wx.EXPAND | wx.ALL)
        sql_browse_sizer = wx.StaticBoxSizer(box_sql_browse, wx.HORIZONTAL)
        sql_browse_sizer.Add(self.sql_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sql_browse_sizer, 0, wx.EXPAND | wx.ALL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.but_save, 0, wx.EXPAND | wx.CENTER, 5)
        buttons_sizer.Add(but_about, 0, wx.EXPAND | wx.CENTER, 5)
        buttons_sizer.Add(but_exit, 0, wx.EXPAND | wx.CENTER, 5)
        sizer.Add(buttons_sizer, 0, wx.EXPAND | wx.ALL)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_FILEPICKER_CHANGED,
                  getattr(self.command, 'db_browse'), self.db_ctrl)
        self.Bind(wx.EVT_FILEPICKER_CHANGED,
                  getattr(self.command, 'sql_browse'), self.sql_ctrl)
        self.Bind(wx.EVT_TOGGLEBUTTON,
                  getattr(self.command, 'connect'), self.but_connect)
        self.Bind(wx.EVT_BUTTON, self.add_table, self.but_add_table)
        self.Bind(wx.EVT_BUTTON, self.insert, self.but_insert)
        self.Bind(wx.EVT_BUTTON, self.update, self.but_update)
        self.Bind(wx.EVT_BUTTON, self.delete, self.but_delete)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'save'), self.but_save)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'about'), but_about)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), but_exit)

        self.but_connect.SetValue(False)
        self.mysql.SetValue(True)
        self.drop_table.SetValue(True)
        self.del_quotes.SetValue(True)
        self.add_db.SetValue(True)
        self.but_add_table.Disable()
        self.but_insert.Disable()
        self.but_update.Disable()
        self.but_delete.Disable()
        self.but_save.Disable()
        self.Layout()

    def add_table(self, event):
        """Run add table dialog."""
        dlg = AddTableDialog(self)
        if wx.ID_OK == dlg.ShowModal():
            table = dlg.table.GetValue()
            self.command.dumper.add_table(table, dlg.params)
        dlg.Destroy()
        self.tables.Set(self.command.dumper.get_tables_names())
        self.Layout()

    def insert(self, event):
        """Run insert dialog."""
        if wx.NOT_FOUND != self.tables.GetSelection():
            dlg = InsertDialog(self)
            if wx.ID_OK == dlg.ShowModal():
                values = []
                for index, value in enumerate(dlg.values):
                    if 'INTEGER' == dlg.params[index][1]:
                        value = value if value is not None else 0
                    values.append((value, dlg.params[index][1]))
                self.command.dumper.insert(dlg.table, values)
            dlg.Destroy()

    def update(self, event):
        """Run update dialog."""
        if wx.NOT_FOUND != self.tables.GetSelection():
            dlg = UpdateDialog(self)
            if wx.ID_CANCEL == dlg.ShowModal():
                dlg.table.cancel_update_db()
            dlg.Destroy()

    def delete(self, event):
        """Run delete dialog."""
        if wx.NOT_FOUND != self.tables.GetSelection():
            dlg = DeleteDialog(self)
            if wx.ID_OK == dlg.ShowModal():
                rows = dlg.grid.GetSelectedRows()
                for row in rows:
                    dlg.grid.DeleteRows(row)
            dlg.Destroy()
