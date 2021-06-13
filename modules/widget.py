# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mylabel import MyLabel #Не забываем импортировать из модуля mylabel.py,
# что хранится в каталоге modules, класс MyLabel, представляющий отдельную ячейку


class Widget(QtWidgets.QWidget):
    """
sudoku
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus) #По умолчанию экземпляр класса QWidget или производного от него класса
        # не может принимать фокус ввода. Чтобы дать ему возможность принимать фокус ввода при щелчке мышью и переходе
        # нажатием клавиши <Tab>, мы вызовем у него метод setFocusPolicy(), передав ему в качестве параметра атрибут StrongFocus.
        #setFocusPolicy(<Способ>) — задает способ получения фокуса компонентом в виде одного из следующих атрибутов класса QtCore.Qt
        #StrongFocus — 11 — получает фокус с помощью клавиши <Tab> и щелчка мышью;
        vBoxMain = QtWidgets.QVBoxLayout() #само поле и набор кнопок будут располагаться друг над другом
        frame1 = QtWidgets.QFrame()
        frame1.setStyleSheet(
            "background-color:#9AA6A7;border:1px solid #9AA6A7;")
        grid = QtWidgets.QGridLayout() #Поле (которое будет создано контейнером-сеткой QGridLayout) мы поместим в панель рамкой QFrame
        grid.setSpacing(0) #setSpacing(<Расстояние>) — задает расстояние между компонентами
        #Создаем сетку QGridLayout, которая сформирует само поле
        idColor = (3, 4, 5, 12, 13, 14, 21, 22, 23,
                   27, 28, 29, 36, 37, 38, 45, 46, 47,
                   33, 34, 35, 42, 43, 44, 51, 52, 53,
                   57, 58, 59, 66, 67, 68, 75, 76, 77)
        #Объявляем массив, хранящий номера ячеек, которые должны быть выделены светло-серым фоном.
        self.cells = [MyLabel(i, MyLabel.colorGrey if i in idColor else
            MyLabel.colorOrange) for i in range(0, 81)]
        #Создаем список из 81-й ячейки MyLabel, сохранив его в атрибуте cells класса Widget. Здесь
        #мы используем выражение генератора списка, которое позволит нам радикально упростить
        #код. Если номер создаваемой ячейки имеется в объявленном ранее массиве, задаем для нее
        #светло-серый цвет фона, в противном случае — оранжевый.
        self.cells[0].setCellFocus()
        self.idCellInFocus = 0
        #Делаем активной ячейку с номером 0 и заносим тот же номер в атрибут idCellInFocus класса Widget.
        # В результате изначально активной станет самая первая ячейка поля
        i = 0 #Помещаем все созданные ячейки в сетку.
        for j in range(0, 9):
            for k in range(0, 9):
                grid.addWidget(self.cells[i], j, k)
                i += 1
        #У всех ячеек задаем для сигнала changeCellFocus обработчик — метод onChangeCellFocus()
        #класса Widget, пока еще не объявленный.
        for cell in self.cells:
            cell.changeCellFocus.connect(self.onChangeCellFocus)
        frame1.setLayout(grid)
        vBoxMain.addWidget(frame1, alignment=QtCore.Qt.AlignHCenter)
        frame2 = QtWidgets.QFrame()
        frame2.setFixedSize(272, 36)
        #Помещаем сетку в панель с рамкой и добавляем последнюю в контейнер VBoxLayout, указав
        #для нее горизонтальное выравнивание по середине.

        hbox = QtWidgets.QHBoxLayout() #кнопки
        hbox.setSpacing(1)
        btns = []
        for i in range(1, 10):
            btn = QtWidgets.QPushButton(str(i))
            btn.setFixedSize(27, 27)
            btn.setFocusPolicy(QtCore.Qt.NoFocus)
            btns.append(btn) # NoFocus) чтобы поле судоку при нажатии любой из этих кнопок
            # не теряло фокус, и пользователь смог продолжать манипулировать в нем с помощью клавиш.
        btn = QtWidgets.QPushButton("X")
        btn.setFixedSize(27, 27)
        btns.append(btn) # кнопку Х, которая уберет цифру из ячейки
        #Помещаем все кнопки в контейнер QHBoxLayout.
        for btn in btns:
            hbox.addWidget(btn)

        #Привязываем к сигналам clicked всех этих кнопок
        #соответствующие обработчики — методы класса поля
        btns[0].clicked.connect(self.onBtn0Clicked)
        btns[1].clicked.connect(self.onBtn1Clicked)
        btns[2].clicked.connect(self.onBtn2Clicked)
        btns[3].clicked.connect(self.onBtn3Clicked)
        btns[4].clicked.connect(self.onBtn4Clicked)
        btns[5].clicked.connect(self.onBtn5Clicked)
        btns[6].clicked.connect(self.onBtn6Clicked)
        btns[7].clicked.connect(self.onBtn7Clicked)
        btns[8].clicked.connect(self.onBtn8Clicked)
        btns[9].clicked.connect(self.onBtnXClicked)

        #Помещаем контейнер с кнопками в панель с рамкой,
        # а ее — во «всеобъемлющий» контейнер VBoxLayout,
        # не забыв указать горизонтальное выравнивание по середине.
        frame2.setLayout(hbox)
        vBoxMain.addWidget(frame2, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(vBoxMain) #помещаем этот контейнер в компонент поля

    def onChangeCellFocus(self, id):
        #Метод onChangeCellFocus() станет обработчиком сигнала changeCellFocus ячейки MyLabel.
        #В качестве единственного параметра он получит номер ячейки, ставшей активной
        if self.idCellInFocus != id and not (id < 0 or id > 80):
            self.cells[self.idCellInFocus].clearCellFocus()
            self.idCellInFocus = id
            self.cells[id].setCellFocus()

    #Переопределенный метод keyPressEvent() будет обрабатывать нажатия клавиш. В качестве
    #параметра он получит экземпляр класса, представляющий событие клавиатуры. Мы сразу
    #же вызовем у этого экземпляра метод key(), чтобы получить код нажатой клавиши. После
    #чего начнем последовательно сравнивать его с кодами различных клавиш, чтобы выяснить,
    #какая из них была нажата
    def keyPressEvent(self, evt):
        key = evt.key()
        if key == QtCore.Qt.Key_Up:
            tid = self.idCellInFocus - 9
            if tid < 0:
                tid += 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Right:
            tid = self.idCellInFocus + 1
            if tid > 80:
                tid -= 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Down:
            tid = self.idCellInFocus + 9
            if tid > 80:
                tid -= 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Left:
            tid = self.idCellInFocus - 1
            if tid < 0:
                tid += 81
            self.onChangeCellFocus(tid)
        elif key >= QtCore.Qt.Key_1 and key <= QtCore.Qt.Key_9:
         self.cells[self.idCellInFocus].setNewText(chr(key)) #Так мы занесем в активную ячейку цифру, соответствующую нажатой клавише
        elif key == QtCore.Qt.Key_Delete or key == QtCore.Qt.Key_Backspace or key == QtCore.Qt.Key_Space:
            self.cells[self.idCellInFocus].setNewText("") #Мы вызываем у активной ячейки метод setNewText(), передав ему пустую строку — так мы уберем цифру с ячейки
        QtWidgets.QWidget.keyPressEvent(self, evt) #мы в обязательном порядке вызываем метод keyPressEvent() базового класса
    def onBtn0Clicked(self):
        self.cells[self.idCellInFocus].setNewText("1")
    def onBtn1Clicked(self):
        self.cells[self.idCellInFocus].setNewText("2")
    def onBtn2Clicked(self):
        self.cells[self.idCellInFocus].setNewText("3")
    def onBtn3Clicked(self):
        self.cells[self.idCellInFocus].setNewText("4")
    def onBtn4Clicked(self):
        self.cells[self.idCellInFocus].setNewText("5")
    def onBtn5Clicked(self):
        self.cells[self.idCellInFocus].setNewText("6")
    def onBtn6Clicked(self):
        self.cells[self.idCellInFocus].setNewText("7")
    def onBtn7Clicked(self):
        self.cells[self.idCellInFocus].setNewText("8")
    def onBtn8Clicked(self):
        self.cells[self.idCellInFocus].setNewText("9")
    def onBtnXClicked(self):
        self.cells[self.idCellInFocus].setNewText("")

    #Метод onClearAllCells() очистит поле судоку. В нем мы перебираем все имеющиеся в поле ячейки,
    # каждую очищаем от занесенной в нее цифры и переводим в разблокированное
    # состояние вызовом метода clearCellBlock() класса MyLabel.
    def onClearAllCells(self):
        for cell in self.cells:
            cell.setText("")
            cell.clearCellBlock()

    #Метод onBlockCell() будет блокировать активную ячейку. Сначала он проверит, есть ли
    #в ней цифра (получить ее можно вызовом унаследованного от суперкласса QLabel метода
    #text()), поскольку блокировать можно только ячейки с цифрами. Если в ячейке нет цифры,
    #на экран будет выведено информационное окно с соответствующим предупреждением.
    #В противном случае будет выполнена проверка, хранится ли в атрибуте isCellChange блокируемой ячейки значение True (т. е. не заблокирована ли уже эта ячейка), и, если это так,
    #ячейка блокируется вызовом метода setCellBlock() класса MyLabel.
    def onBlockCell(self):
        cell = self.cells[self.idCellInFocus]
        if cell.text() == "":
            QtWidgets.QMessageBox.information(self, "Судоку",
                                              "Нельзя блокировать пустую ячейку")
        else:
            if cell.isCellChange:
                cell.setCellBlock()

    #выполняет перебор всех ячеек и блокирует любую из них,
    # если она содержит цифру и еще не заблокирована
    def onBlockCells(self):
        for cell in self.cells:
            if cell.text() and cell.isCellChange:
                cell.setCellBlock()

    # предназначенный для разблокирования активной ячейки, предварительно проверит,
    # хранится ли в ее атрибуте isCellChange значение False (т. е. заблокирована ли эта ячейка).
    # И только после этого он вызывает метод clearCellBlock() класса
    #MyLabel, чтобы разблокировать ячейку
    def onClearBlockCell(self):
        cell = self.cells[self.idCellInFocus]
        if not cell.isCellChange:
            cell.clearCellBlock()

    def onClearBlockCells(self):
        for cell in self.cells:
            if not cell.isCellChange:
                cell.clearCellBlock()

    #Метод getDataAllCells() возвращает строку с данными
    # о головоломке в полном формате.
    def getDataAllCells(self):
        listAllData = []
        for cell in self.cells:
            listAllData.append("0" if cell.isCellChange else "1")
            s = cell.text() #извлекаем текстовое содержимое ячейки
            listAllData.append(s if len(s) == 1 else "0")#, проверяем, равна ли ее длина единице (т. е. установлена ли в ячейку цифра
        return "".join(listAllData) #вернуть строку из списка

    def getDataAllCellsMini(self):
        listAllData = []
        for cell in self.cells:
            s = cell.text()
            listAllData.append(s if len(s) == 1 else "0")
        return "".join(listAllData)

    def getDataAllCellsExcel(self):
        numbers = (9, 18, 27, 36, 45, 54, 63, 72)
        listAllData = [self.cells[0].text()]
        for i in range(1, 81):
            listAllData.append("\r\n" if i in numbers else "\t")
            listAllData.append(self.cells[i].text())
        listAllData.append("\r\n")
        return "".join(listAllData)

    def setDataAllCells(self, data):
        l = len(data)
        if l == 81:
            for i in range(0, 81):
                if data[i] == "0":
                    self.cells[i].setText("")
                    self.cells[i].clearCellBlock()
                else:
                    self.cells[i].setText(data[i])
                    self.cells[i].setCellBlock()
            self.onChangeCellFocus(0)
        elif l == 162:
            for i in range(0, 162, 2):
                if data[i] == "0":
                    self.cells[i // 2].clearCellBlock() #Номер ячейки мы можем получить,
                else:                                           #разделив номер очередного символа на 2 нацело
                    self.cells[i // 2].setCellBlock()
                self.cells[i // 2].setText("" if data[i + 1] == "0"
                                           else data[i + 1])
            self.onChangeCellFocus(0) #после вставки данных мы делаем активной
            # самую первую (левую верхнюю) ячейку поля судоку

    def print(self, printer):
        #создаем два пера: для вывода цифр (черное) и рамок ячеек (темно-серое)
        # и две кисти: оранжевую и светло-серую.
        penText = QtGui.QPen(QtGui.QColor(MyLabel.colorBlack), 1)
        penBorder = QtGui.QPen(QtGui.QColor(QtCore.Qt.darkGray), 1)
        brushOrange = QtGui.QBrush(QtGui.QColor(MyLabel.colorOrange))
        brushGrey = QtGui.QBrush(QtGui.QColor(MyLabel.colorGrey))
        #Начинаем печать
        painter = QtGui.QPainter()
        painter.begin(printer)
        #Указываем шрифт для вывода цифр в ячейках
        painter.setFont(QtGui.QFont("Verdana", pointSize=14))
        #Объявляем переменную, в которой будет храниться номер печатаемой яч
        i = 0
        for j in range(0, 9): #строки
            for k in range(0, 9): #ячейки
                x = j * 30 #координаты левого верхнего угла печатаемой
                y = k * 30 # в настоящий момент ячейки
                painter.setPen(penBorder) #темно-серое перо печати рамки этого квадратика
                painter.setBrush(brushGrey  #Если для фона ячейки задан
                                     if self.cells[i].bgColorDefault == MyLabel.colorGrey
                                     else brushOrange) #светло-серый цвет, задаем светло-серое перо
                                     # в противном случае — оранжевое
                painter.drawRect(x, y, 30, 30) #Выводим квадратик
                painter.setPen(penText) # черное перо, которым будет выведена цифра
                painter.drawText(x, y, 30, 30, QtCore.Qt.AlignCenter,
                                 self.cells[i].text()) #Выводим поверх квадратика цифру, установленную в ячейку
                i += 1
        painter.end() #завершаем печать
