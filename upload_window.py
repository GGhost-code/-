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
            if not number.isdigit():
                QMessageBox.critical(self, 'Ошибка', "В номере обнаружена буква или специальный символ")
            elif len(number) != 11:
                QMessageBox.critical(self, 'Ошибка', "Номер телефона либо слишком короткий, либо слишком длинный")
            else:
                QMessageBox.critical(self, 'Ошибка', "Номер начинается с неправильного индекса страна")
            return
        if not filename:
            QMessageBox.critical(self, 'Ошибка', "Не выбран файл с фото")
            return
        if number[0] == "8":
            number = "7" + number[1:]
        photo_id = uuid0.generate()
        self.save_image(filename, photo_id)
        category_id = self.cur.execute(
            f'SELECT Id FROM categories WHERE name = "{category}"').fetchall()[0][0]
        check = f'SELECT * FROM things WHERE name == "{name}" AND category_id == {category_id} AND phone == "{number}"'
        res = self.cur.execute(check).fetchall()
        type = 1
        if res:
            query = f'UPDATE things SET filename_id="{photo_id}" WHERE name == "{name}" AND category_id' \
                    f' == {category_id} AND phone == "{number}"'
            type = 0
        else:
            query = f'INSERT INTO things (name, category_id, phone, filename_id) VALUES ("{name}", {category_id},' \
                f' "{number}", "{photo_id}")'
        self.cur.execute(query)
        self.db.commit()
        self.reset()
        if type:
            QMessageBox.information(self, "Поздравляю", "Ваше объявление успешно подано!")
        else:
            QMessageBox.information(self, "Поздравляю", "Ваше объявление успешно изменено!")

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
        image = Image.open(filename)
        to_save = None
        x, y = image.size
        x1, x2 = 700, 450
        size1 = x / y
        size2 = x1 / x2
        if size1 > size2:
            sizex = x1 / x
            height = int(sizex * y)
            to_save = image.resize((x1, height))
        elif size1 < size2:
            sizex = x2 / y
            width = int(sizex * x)
            to_save = image.resize((width, x2))
        to_save.save(f'images/{id}.png')

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
