import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QTableWidget, QPushButton, QComboBox, QLineEdit, QLabel, QInputDialog)


class PhotoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows_ui/photo.ui', self)  # Загружаем дизайнs
        self.db = sqlite3.connect("database.sqlite")
        self.cur = self.db.cursor()
        self.setWindowTitle("Фото")

    def initUi(self, filename, id):
        self.id = id
        self.photo.setPixmap(QPixmap(f'images/{filename}'))
        self.take.clicked.connect(self.delete)

    def getText(self): # Проверка уверенности
        text, okPressed = QInputDialog.getText(self, "Подтверждение", "Вы уверены? Запись будет удалена.", QLineEdit.Normal, "")
        if okPressed and text.lower() == 'да':
            return True

    def delete(self): # Удалить объявление из БД
        if self.getText():
            id = self.id
            self.cur.execute(f'DELETE FROM things WHERE id = {id}')
            self.db.commit()
            self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhotoWindow()
    ex.show()
    sys.exit(app.exec_())
