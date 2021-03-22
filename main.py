import sys
import os
import sqlite3
import AddContact
import EditContact
import deleteContact

from PySide2.QtWidgets import *
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtGui


class phonebook(QWidget):
    def __init__(self):
        super(phonebook, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.show()
        self.conectDB()
        self.ui.add_btn.clicked.connect(self.openAddDg)
        self.ui.del_btn.clicked.connect(deleteContact.deleteContact)
        self.ui.edit_btn.clicked.connect(self.editContact)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def conectDB(self):
        self.conn = sqlite3.connect('contacts.db')
        c = self.conn.cursor()
        c.execute('SELECT * FROM contacts WHERE deleted = 0')
        c2 = self.conn.cursor()
        c2.execute('SELECT name, phonenumber FROM contacts WHERE deleted = 0')

        # start show table data
        self.allSQLRows = c.fetchall()
        self.ui.tableWidget.setRowCount(len(self.allSQLRows))
        self.ui.tableWidget.setColumnCount(2)

        row = 0
        while True:
            sqlRow = c2.fetchone()
            if sqlRow == None:
                break
            for col in range(0, 2):
                self.ui.tableWidget.setItem(
                    row, col, QTableWidgetItem(str(sqlRow[col])))
            row += 1
        # end show table data

    def openAddDg(self):
        self.addClass = AddContact.AddContact()

    def editContact(self):
        self.editClass = EditContact.EditContact(
            self.allSQLRows[self.ui.tableWidget.currentIndex().row()][1])


if __name__ == "__main__":
    app = QApplication([])
    widget = phonebook()
    sys.exit(app.exec_())
