from PyQt5 import QtCore, QtWidgets, QtGui


class MyLabel(QtWidgets.QLabel):
    colorYellow = "#FFFF90"
    colorOrange = "#F5D8C1"
    colorGrey = "#E8E8E8"
    colorBlack = "#000000"
    colorRed = "#D77A38"
    changeCellFocus = QtCore.pyqtSignal(int)

    def __init__(self, id, bgColor, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(30, 30)
        self.setMargin(0)
        self.setText("")
        if id < 0 or id > 80:
            id = 0
        self.id = id
        self.isCellChange = True
        self.fontColorCurrent = self.colorBlack
        self.bgColorDefault = bgColor
        self.bgColorCurrent = bgColor

    def mousePressEvent(self, evt: QtGui.QMouseEvent) -> None: #в методе mousePressEvent(),
        # выполнив все необходимые действия, а именно, сгенерировав сигнал changeCellFocus,
        # мы в обязательном порядке вызываем тот же метод суперкласса. Если этого не сделать, возможны проблемы
        self.changeCellFocus.emit(self.id)
        QtWidgets.QLabel.mousePressEvent(self, evt)

    def showColorCurrent(self):
        self.setStyleSheet("background-color:" + self.bgColorCurrent +
                           ";color:" + self.fontColorCurrent + ";") #привязываем к нашему компоненту
        # таблицу стилей, которая установит для ячейки цвета текста и фона.

    def setCellFocus(self):
        self.bgColorCurrent = self.colorYellow
        self.showColorCurrent()

    def clearCellFocus(self):
        self.bgColorCurrent = self.bgColorDefault
        self.showColorCurrent()

    def setCellBlock(self):
        self.isCellChange = False
        self.fontColorCurrent = self.colorRed
        self.showColorCurrent()

    def clearCellBlock(self):
        self.isCellChange = True
        self.fontColorCurrent = self.colorBlack
        self.showColorCurrent()

    def setNewText(self, text):
        if self.isCellChange:
            self.setText(text)