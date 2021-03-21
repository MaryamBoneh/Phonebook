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
        self.ui.del_btn.clicked.connect(self.deleteContact)
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
        self.addClass = AddContact()

    def editContact(self):
        self.editClass = EditContact(
            self.allSQLRows[self.ui.tableWidget.currentIndex().row()][1])

    def deleteContact(self):

        row = self.ui.tableWidget.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self, "Warning!", "Do you want to remove the selected contact?", QMessageBox.Ok | QMessageBox.Cancel,)

        if messageBox == QMessageBox.Ok:
            sql = 'DELETE FROM contacts WHERE phonenumber=?'
            cur = self.conn.cursor()
            cur.execute(sql, (self.allSQLRows[row][1],))
            self.conn.commit()


class AddContact(QWidget):
    def __init__(self):
        super(AddContact, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("add-contact.ui")
        self.ui.show()

        self.conectDB()
        self.ui.insert_btn.clicked.connect(self.InsertRow)
        self.ui.cancle_btn.clicked.connect(self.ui.close)

    def conectDB(self):
        self.conn = sqlite3.connect('contacts.db')

    def InsertRow(self):
        name = self.ui.name_txt.toPlainText()
        phonenumber = self.ui.phone_txt.toPlainText()

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO contacts (name, phonenumber, deleted)"
                        "VALUES('%s', '%s', '%s')" % (''.join(name), ''.join(phonenumber), 0))

            self.ui.close()
            self.close()


class EditContact(QWidget):
    def __init__(self, pn):
        super(EditContact, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("add-contact.ui")
        self.ui.show()
        self.oldpn = pn
        self.conectDB()
        self.ui.insert_btn.clicked.connect(self.EditRow)
        self.ui.cancle_btn.clicked.connect(self.ui.close)

    def conectDB(self):
        self.conn = sqlite3.connect('contacts.db')

    def EditRow(self):
        name = self.ui.name_txt.toPlainText()
        phonenumber = self.ui.phone_txt.toPlainText()

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("UPDATE contacts SET name = '%s', phonenumber = '%s' WHERE phonenumber = '%s'" %
                        (''.join(name), ''.join(phonenumber), self.oldpn))

            self.ui.close()
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = phonebook()
    sys.exit(app.exec_())
