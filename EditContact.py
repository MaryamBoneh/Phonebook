import sqlite3
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
import main


class EditContact(QWidget):
    def __init__(self, pn):
        super(EditContact, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("add-contact.ui")
        self.ui.caption_label.setText('Edit Contact')
        self.ui.insert_btn.setText('Save')
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

        main.widget.conectDB()
        self.ui.close()
        self.close()
