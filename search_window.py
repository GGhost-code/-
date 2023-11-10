import sqlite3
import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTableWidgetItem

from photo_window import PhotoWindow


class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows_ui/search.ui', self)
        self.initUi()
        self.db = sqlite3.connect("database.sqlite")
        self.cur = self.db.cursor()
        self.test = QLabel
        self.setWindowTitle("Потеряшка")

    def initUi(self):
        self.searchBtn.clicked.connect(self.search)
        self.resetBtn.clicked.connect(self.reset)
        self.resComp.clicked.connect(self.out)
        self.photo_window = PhotoWindow()

    def out(self): # Вывод результата запроса в файл
        pass

    def open_photo(self, filename, id): # Открыть фото для просмотра
        def result():
            self.photo_window.initUi(filename, id)
            print(filename)
            self.photo_window.show()

        return result

    def reset(self): # Сбосить фильтры
        self.searchEdit.setText('')
        self.combo_search.setCurrentIndex(0)
        self.table.setRowCount(0)

    def search(self): # Поиск
        name = self.searchEdit.text()
        category = self.combo_search.currentText()
        if category == "Любая":
            category = None
        query = f'SELECT * FROM things'
        if name or category:
            pass
            query += " WHERE"
            if name:
                query += f' name LIKE "{name}%"'
                if category:
                    query += " AND"
            if category:
                query += f' category_id == {self.getCategoryId(category)}'

        print(query)

        result = self.cur.execute(query).fetchall()

        for i in result:
            print(i)

        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            print(i, row)
            self.table.setItem(i, 0, QTableWidgetItem(row[1]))
            self.table.setItem(i, 1, QTableWidgetItem(self.getCategoryName(row[2])))
            correct_number = self.make_number_correct(row[3])
            self.table.setItem(i, 2, QTableWidgetItem(correct_number))
            button = QPushButton('Открыть', self)
            # self.filename = row[4]
            button.clicked.connect(self.open_photo(row[4], row[0]))
            self.table.setCellWidget(i, 3, button)

    def getCategoryId(self, category): # Найти ID категории по названию
        if category == "Вещи":
            return 1
        elif category == "Одежда":
            return 2
        elif category == "Животные":
            return 3
        else:
            return 4

    def getCategoryName(self, id): # Найти название категории по ID
        if id == 1:
            return "Вещи"
        elif id == 2:
            return "Одежда"
        elif id == 3:
            return "Животные"
        else:
            return "Другое"

    def make_number_correct(self, number): # Сделать номер телефона корректным
        if number[0] == "8":
            number = "+7" + number[1:]
        else:
            number = "+" + number
        number = number[:2] + " " + number[2:]
        number = number[:6] + " " + number[6:]
        number = number[:10] + "-" + number[10:]
        number = number[:13] + "-" + number[13:]
        return number


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchWindow()
    ex.show()
    sys.exit(app.exec_())
