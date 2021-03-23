import sqlite3
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import *


class deleteContact(QWidget):
    def __init__(self, phonebook):
        super(deleteContact, self).__init__()
        self.pb = phonebook
        self.conn = sqlite3.connect('contacts.db')

        row = self.pb.ui.tableWidget.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self, "Warning!", "Do you want to remove the selected contact?", QMessageBox.Ok | QMessageBox.Cancel,)

        if messageBox == QMessageBox.Ok:
            try:
                sql = 'DELETE FROM contacts WHERE phonenumber=?'
                cur = self.conn.cursor()
                cur.execute(sql, (phonebook.connectdb.allSQLRows[row][1],))
                self.conn.commit()
                self.pb = phonebook
                self.pb.conectDB()

            except Exception as e:
                print("error:", e)
