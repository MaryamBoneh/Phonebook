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

        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.show()

        self.conectDB()
        self.ui.add_btn.clicked.connect(self.openAddDg)

    def conectDB(self):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('SELECT * FROM contacts WHERE deleted = 0')
        c2 = conn.cursor()
        c2.execute('SELECT * FROM contacts WHERE deleted = 0')

        # start show table data
        self.allSQLRows = c.fetchall()
        self.ui.tableWidget.setRowCount(len(self.allSQLRows))
        self.ui.tableWidget.setColumnCount(3)

        row = 0
        while True:
            sqlRow = c2.fetchone()
            if sqlRow == None:
                break
            for col in range(0, 3):
                self.ui.tableWidget.setItem(
                    row, col, QTableWidgetItem(str(sqlRow[col])))
            row += 1
        # end show table data

    def openAddDg(self):
        self.addClass = AddContact()
        self.addClass.load_ui()


class AddContact(QWidget):
    def __init__(self):
        super(AddContact, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load("add-contact.ui")
        self.ui.show()

        self.conectDB()
        self.ui.insert_btn.clicked.connect(self.InsertRow)

    def conectDB(self):
        self.conn = sqlite3.connect('contacts.db')

    def InsertRow(self):
        name = self.ui.name_txt.toPlainText()
        phonenumber = self.ui.phone_txt.toPlainText()

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO contacts (name, phonenumber, deleted)"
                        "VALUES('%s', '%s', '%s')" % (''.join(name), ''.join(phonenumber), 0))

            QMessageBox.about(self, 'Connection',
                              'Data Inserted Successfully!!')
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = phonebook()
    sys.exit(app.exec_())
