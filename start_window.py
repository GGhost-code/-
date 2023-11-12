import sqlite3
import os

from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *

from search_window import SearchWindow
from upload_window import UploadWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows_ui/main.ui', self)  # Загружаем дизайнs
        if not os.path.exists("database.sqlite"):
            self.create_db()
        self.setWindowTitle("Потеряшка")
        bar = self.menuBar()
        self.reference = bar.addMenu("Справка")
        self.opre = QAction("Открыть справку", self)
        self.opre.triggered.connect(self.open_ref)
        self.reference.addAction(self.opre)
        self.saveref = QAction("Сохранить справку", self)
        self.saveref.triggered.connect(self.getFolderName)
        self.reference.addAction(self.saveref)
        self.createImageFolder()
        self.ref_text = '''
            Проект “Потеряшка”
            Выполнял ученик 9 О класса
            Котлярский Павел Юрьевич

            Часто теряете вещи и вообще не имеете понятия, где их искать? А вдруг их уже кто - то нашел? Чтобы у Вас 
            даже не возникали такие вопросы, было создано приложение “Потеряшка”. В нем вы сможете найти и забрать 
            потерянные вещи, а также помочь другим людям, если вы нашли забытую вещь, добавив ее в базу данных.

            Как пользоваться приложением: 
            Если вы что - то нашли, выберите в меню "Я что - то нашел" 
            Нажмите на кнопку "Начать" 
            В полях на окне введите нужные значения
            Критерии к значениям: 
                Имя должно состоять хотя бы из одной буквы.
                Номер телефона должен: 
                    Быть российским 
                    Начинаться на 8 или +7 
                    Состоять из 11 цифр 
            Фотография обязательно должна быть подгружена. Если вы введете название, категорию и номер телефона те, 
            какие уже есть в базе данных, то вы можете изменить объявление, поменяв в нем изображение

            Если вы что - то потеряли, выберите в меню "Я что - то потерял"
            Нажмите на кнопку "Начать"
            Введите желаемые значения
            Нажмите "Поиск"
            Если вы хотите посмотреть изображение, то нажмите на кнопку "Открыть" в результате поиска'''
        self.initUi()

    def initUi(self):
        self.start.clicked.connect(self.begin)
        self.search_window = SearchWindow()
        self.upload_window = UploadWindow()

    def begin(self):  # В зависимости от выбора запустить окно
        if self.comboChoose.currentIndex() == 1:
            self.search_window.show()
        else:
            self.upload_window.show()

    def create_db(self):  # Создаем базу данных, если таковой нету
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

    def getFolderName(self):
        try:
            folderpath = QFileDialog.getExistingDirectory(self, "Открыть")
            f = open(folderpath + "/reference.txt", 'w')
            f.write(self.ref_text)
            f.close()
        except:
            QMessageBox.critical(self, 'Ошибка', "Не выбрана папка")

    def createImageFolder(self):
        if not os.path.exists('images'):
            os.mkdir('images')


    def open_ref(self):
        os.chdir("others")
        os.startfile("reference.txt")
        os.chdir("../")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec_())
