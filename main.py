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
        self.ui.add_btn.clicked.connect(openAddDg)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def conectDB(self):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('SELECT * FROM contacts WHERE deleted = 0')
        c2 = conn.cursor()
        c2.execute('SELECT * FROM contacts WHERE deleted = 0')

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


def openAddDg():
    global addClass
    addClass = AddContact()
    addClass.load_ui()


class AddContact(QWidget):
    def __init__(self):
        super(AddContact, self).__init__()
        self.load_ui()
        self.conectDB()
        self.ui.insert_btn.clicked.connect(self.InsertRow)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "add-contact.ui")
        print(path)
        dg_ui_file = QFile(path)
        dg_ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(dg_ui_file, self)
        dg_ui_file.close()

    def conectDB(self):
        self.conn = sqlite3.connect('contacts.db')

    def InsertRow(self):
        name = self.ui.name_txt.toPlainText()
        phonenumber = self.ui.phone_txt.toPlainText()
        
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO contacts (name, phonenumber, deleted)"
                        "VALUES('%s', '%s', '%s')" % (''.join(name),''.join(phonenumber), 0))

            QMessageBox.about(self, 'Connection', 'Data Inserted Successfully!!')
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = phonebook()
    widget.show()
    sys.exit(app.exec_())
