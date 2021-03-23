import sys
import os
import database
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
        self.ui.add_btn.clicked.connect(self.addContact)
        self.ui.del_btn.clicked.connect(self.delContact)
        self.ui.edit_btn.clicked.connect(self.editContact)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
    def conectDB(self):
        self.connectdb = database.database(self)

    def addContact(self):
        self.addClass = AddContact.AddContact(self)

    def editContact(self):
        if self.ui.tableWidget.currentIndex().row() > 0:
            self.editClass = EditContact.EditContact(
                self.connectdb.allSQLRows[self.ui.tableWidget.currentIndex().row()][1], self)
        else:
            messageBox = QMessageBox.warning(
                self, "Error", "Please Select A Contact", QMessageBox.Ok)

    def delContact(self):
        if self.ui.tableWidget.currentIndex().row() > 0:
            self.delClass = deleteContact.deleteContact(self)
        else:
            messageBox = QMessageBox.warning(
                self, "Error", "Please Select A Contact", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication([])
    widget = phonebook()
    sys.exit(app.exec_())
