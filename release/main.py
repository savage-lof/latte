import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
import sqlite3
from release.ui_file import Ui_Form
from release.addEditCoffeeForm import Ui_Forms


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("../data/coffee.db")
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""SELECT name, degree, ground, description, price, volume 
                                          FROM Espresso""").fetchall()
        self.select_data()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.add)
        self.window_add = None

    def select_data(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.result):
            self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))

    def add(self):
        self.window_add = Add(self.sender().text())
        self.window_add.show()
        self.close()


class Add(QWidget, Ui_Forms):
    def __init__(self, push):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("../data/coffee.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.exit)
        self.ex = None
        self.push = push

    def connect(self):
        name = f'{self.name.text()}|name'
        degree = f'{self.degree.text()}|degree'
        ground = f'{self.ground.text()}|ground'
        description = f'{self.description.text()}|description'
        price = f'{self.price.text()}|price'
        volume = f'{self.volume.text()}|volume'
        if self.push == 'Добавить':
            self.cur.execute('''INSERT INTO 
                                Espresso(name, degree, ground, description, price, volume) 
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (name.split('|')[0], degree.split('|')[0], ground.split('|')[0],
                              description.split('|')[0], price.split('|')[0], volume.split('|')[0])).fetchall()
        else:
            id = self.id.text()
            for i in (name, degree, ground, description, price, volume):
                b = i.split('|')[0]
                if str(b).endswith('*'):
                    sat = b[:len(b) - 1]
                    abc = i.split()[1]
                    break
            que = f'''UPDATE Espresso
                      SET {abc} = '{sat}'
                      WHERE id = {id}'''
            self.cur.execute(que).fetchall()
        self.con.commit()
        self.exit()

    def exit(self):
        self.ex = MyWidget()
        self.ex.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
