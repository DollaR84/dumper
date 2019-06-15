"""
Commands for graphical interface.

Created on 16.03.2018

@author: Ruslan Dolovanyuk

"""

from dialogs.dialogs import About
from dialogs.dialogs import Message


class Commands:
    """Helper class, contains command for bind events, menu and buttons."""

    def __init__(self, drawer, dumper):
        """Initilizing commands class."""
        self.drawer = drawer
        self.dumper = dumper
        self.message = Message(self.drawer)

    def db_browse(self, event):
        """Change file database sqlite."""
        self.drawer.path = self.drawer.db_ctrl.GetPath()

    def sql_browse(self, event):
        """Change file dump file for save."""
        self.drawer.path_sql = self.drawer.sql_ctrl.GetPath()

    def connect(self, event):
        """Connect sqlite database."""
        if self.drawer.but_connect.GetValue():
            self.dumper.start(self.drawer.path)
            self.drawer.tables.Set(self.dumper.get_tables_names())
            self.drawer.but_add_table.Enable()
            self.drawer.but_insert.Enable()
            self.drawer.but_update.Enable()
            self.drawer.but_delete.Enable()
            self.drawer.but_save.Enable()
            self.drawer.but_connect.SetLabel('Отключить')
        else:
            self.dumper.finish()
            self.drawer.tables.Set([])
            self.drawer.but_add_table.Disable()
            self.drawer.but_insert.Disable()
            self.drawer.but_update.Disable()
            self.drawer.but_delete.Disable()
            self.drawer.but_save.Disable()
            self.drawer.but_connect.SetLabel('Подключить')
        self.drawer.Layout()

    def save(self, event):
        """Save dump sql database in file."""
        if '' == self.drawer.path_sql:
            self.message.error('Ошибка', 'Имя файла дампа не указано')
            return
        self.dumper.dump(self.drawer.path_sql)
        if self.drawer.mysql.GetValue():
            self.dumper.fix_mysql(self.drawer.path_sql)
        if self.drawer.drop_table.GetValue():
            self.dumper.add_drop_tables(self.drawer.path_sql)
        if self.drawer.del_quotes.GetValue():
            self.dumper.del_quotes_around_table_name(self.drawer.path_sql)
        if self.drawer.use_db.GetValue():
            self.dumper.use_database_name(self.drawer.path_sql)
        elif self.drawer.add_db.GetValue():
            self.dumper.add_database_name(self.drawer.path_sql)
        self.message.information('Сохранение', 'Файл дампа успешно сохранен')

    def about(self, event):
        """Run about dialog."""
        About(self.drawer,
              'О программе...',
              'Конструктор дампов базы данных',
              '1.0',
              'Руслан Долованюк').ShowModal()

    def close(self, event):
        """Close event for button close."""
        self.drawer.Close(True)

    def close_window(self, event):
        """Close window event."""
        self.drawer.Destroy()
