from PySide2.QtWidgets import QMessageBox
import main


def deleteContact(self):

    row = main.phonebook.ui.tableWidget.currentIndex().row()
    if row < 0:
        return

    messageBox = QMessageBox.warning(
        self, "Warning!", "Do you want to remove the selected contact?", QMessageBox.Ok | QMessageBox.Cancel,)

    if messageBox == QMessageBox.Ok:
        sql = 'DELETE FROM contacts WHERE phonenumber=?'
        cur = self.conn.cursor()
        cur.execute(sql, (main.phonebook.allSQLRows[row][1],))
        self.conn.commit()
        main.phonebook.widget.conectDB()
