import sqlite3
from PySide2.QtWidgets import *


class database(QWidget):
    def __init__(self, phonebook):
        super(database, self).__init__()
        self.conn = sqlite3.connect('contacts.db')
        c = self.conn.cursor()
        c.execute('SELECT * FROM contacts WHERE deleted = 0')
        c2 = self.conn.cursor()
        c2.execute('SELECT name, phonenumber FROM contacts WHERE deleted = 0')
        self.pb = phonebook

        # show table data
        self.allSQLRows = c.fetchall()
        self.pb.ui.tableWidget.setRowCount(len(self.allSQLRows))
        self.pb.ui.tableWidget.setColumnCount(2)
        row = 0
        while True:
            sqlRow = c2.fetchone()
            if sqlRow == None:
                break
            for col in range(0, 2):
                self.pb.ui.tableWidget.setItem(
                    row, col, QTableWidgetItem(str(sqlRow[col])))
            row += 1
