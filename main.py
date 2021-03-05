import sys
import os
import sqlite3

from PySide2.QtWidgets import *
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtGui


class phonebook(QWidget):
    def __init__(self):
        super(phonebook, self).__init__()
        self.load_ui()
        self.conectDB()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def conectDB(self):
        conn = sqlite3.connect('phonebook/contacts.db')
        c = conn.cursor()
        c.execute('SELECT * FROM contacts')
        c2 = conn.cursor()
        c2.execute('SELECT * FROM contacts')

        self.allSQLRows = c.fetchall()
        self.ui.tableWidget.setRowCount(len(self.allSQLRows))
        self.ui.tableWidget.setColumnCount(4)

        row = 0
        while True:
            sqlRow = c2.fetchone()
            if sqlRow == None:
                break
            for col in range(0, 4):
                self.ui.tableWidget.setItem(
                    row, col, QTableWidgetItem(str(sqlRow[col])))
            row += 1


if __name__ == "__main__":
    app = QApplication([])
    widget = phonebook()
    widget.show()
    sys.exit(app.exec_())
