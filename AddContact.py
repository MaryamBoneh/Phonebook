import sqlite3
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *


class AddContact(QWidget):
    def __init__(self, phonebook):
        super(AddContact, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("add-contact.ui")
        self.ui.show()
        self.pb = phonebook

        self.conectDB()
        self.ui.insert_btn.clicked.connect(self.InsertRow)
        self.ui.cancle_btn.clicked.connect(self.ui.close)

    def conectDB(self):
        self.conn = sqlite3.connect('contacts.db')

    def InsertRow(self):
        try:
            name = self.ui.name_txt.toPlainText()
            phonenumber = self.ui.phone_txt.toPlainText()

            with self.conn:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO contacts (name, phonenumber, deleted)"
                            "VALUES('%s', '%s', '%s')" % (''.join(name), ''.join(phonenumber), 0))

            self.pb.conectDB()
            self.ui.close()
            self.close()

        except Exception as e:
            print("error:", e)
