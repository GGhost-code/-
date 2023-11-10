import sys
import sqlite3
from PIL import Image
import uuid0
import os

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QPushButton, QComboBox, QFileDialog


class UploadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows_ui/upload.ui', self)  # Загружаем дизайн
        self.initUi()
        self.db = sqlite3.connect("database.sqlite")
        self.cur = self.db.cursor()
        self.test = QLineEdit
        self.setWindowTitle("Потеряшка")

    def initUi(self):
        self.uploadAll.clicked.connect(self.upload)
        self.uploadPhoto.clicked.connect(self.getDirectory)

    def upload(self): # Загрузить результат в БД
        name = self.nameEdit.text()
        category = self.comboUpload.currentText()
        number = self.phoneEdit.text()
        number = str(number).replace("+", "").replace("-", "").replace("(", "").replace(")", ""). \
            replace(" ", "")
        filename = self.uploadName.text()
        if not name:
            QMessageBox.critical(self, 'Ошибка', "Не указано название предмета")
            return
        if not number.isdigit() or len(number) != 11 or (number[0] != "7" and number[0] != "8"):
            QMessageBox.critical(self, 'Ошибка', "Неправильно набран номер телефона")
            return
        if not filename:
            QMessageBox.critical(self, 'Ошибка', "Не выбран файл с фото")
            return
        id = uuid0.generate()
        self.save_image(filename, id)
        category_id = self.cur.execute(
            f'SELECT Id FROM categories WHERE name = "{category}"').fetchall()[0][0]
        query = f'INSERT INTO things (name, category_id, phone, filename_id) VALUES ("{name}", {category_id},' \
                f' "{number}", "{id}")'
        self.cur.execute(query)
        self.db.commit()
        self.reset()
        QMessageBox.information(self, "Поздравляю", "Ваше объявление успешно подано!")

    def update_filename(self): # Установить новое имя файла в соответствующей строке
        self.uploadName.setText(self.filename)

    def getDirectory(self):  # Вызов диалогового окна выбора файла
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "JPEG Files(*.jpeg);;\
                                                         PNG Files(*.png);;GIF File(*.gif);;All Files(*)")

        self.filename = filename
        self.update_filename()

    def save_image(self, filename, id): # Сохранить изображение
        im = Image.open(filename)
        im2 = None
        x, y = im.size
        nx, ny = 700, 450
        nratio = nx / ny
        ratio = x / y
        if ratio > nratio:
            xratio = nx / x
            height = int(xratio * y)
            im2 = im.resize((nx, height))
        elif ratio < nratio:
            yratio = ny / y
            width = int(yratio * x)
            im2 = im.resize((width, ny))
        im2.save(f'images/{id}.png')

    def reset(self): # Сбросить всё
        self.uploadName.setText("")
        self.nameEdit.setText("")
        self.comboUpload.setCurrentIndex(0)
        self.phoneEdit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UploadWindow()
    ex.show()
    sys.exit(app.exec_())
