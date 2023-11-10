import sqlite3
import sys
from os import path

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow)

from search_window import SearchWindow
from upload_window import UploadWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows_ui/main.ui', self)  # Загружаем дизайнs
        if not path.exists("database.sqlite"):
            self.create_db()
        self.initUi()
        self.setWindowTitle("Потеряшка")

    def initUi(self):
        self.start.clicked.connect(self.begin)
        self.search_window = SearchWindow()
        self.upload_window = UploadWindow()

    def begin(self): # В зависимости от выбора запустить окно
        if self.comboChoose.currentIndex() == 1:
            self.search_window.show()
        else:
            self.upload_window.show()

    def create_db(self): # Создаем базу данных, если таковой нету
        file = open("database.sqlite", mode='wb')
        file.close()
        del file
        db = sqlite3.connect('database.sqlite')
        cur = db.cursor()
        cur.execute(
            'CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name text);').fetchall()
        cur.execute('CREATE TABLE things (id INTEGER PRIMARY KEY AUTOINCREMENT, name text,'
                    ' category_id integer, phone text, filename_id text)').fetchall()
        cur.execute('INSERT INTO categories (name) VALUES ("Вещи"),'
                    ' ("Одежда"), ("Животные"), ("Другое")').fetchall()
        db.commit()
        db.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec_())
