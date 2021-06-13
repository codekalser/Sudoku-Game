from PyQt5 import QtCore, QtWidgets, QtPrintSupport


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Предварительный просмотр")
        self.resize(600, 400)
        vBox = QtWidgets.QVBoxLayout()
        hBox1 = QtWidgets.QHBoxLayout()
        btnZoomIn = QtWidgets.QPushButton("&+")
        btnZoomIn.setFocusPolicy(QtCore.Qt.NoFocus)
        hBox1.addWidget(btnZoomIn, alignment=QtCore.Qt.AlignLeft)
        btnZoomOut = QtWidgets.QPushButton("&-")
        btnZoomOut.setFocusPolicy(QtCore.Qt.NoFocus)
        hBox1.addWidget(btnZoomOut, alignment=QtCore.Qt.AlignLeft)
        btnZoomReset = QtWidgets.QPushButton("&Сброс")
        btnZoomReset.setFocusPolicy(QtCore.Qt.NoFocus)
        btnZoomReset.clicked.connect(self.zoomReset)
        hBox1.addWidget(btnZoomReset, alignment=QtCore.Qt.AlignLeft)
        #Добавляем в горизонтальный контейнер растягивающуюся область,
        # чтобы все кнопки оказались прижатыми к левому краю контейнера.
        hBox1.addStretch() #Добавляем сам горизонтальный контейнер в вертикальный
        hBox2 = QtWidgets.QHBoxLayout() #будут выводиться панель предварительного
        # просмотра и кнопка Закрыть
        self.ppw = QtPrintSupport.QPrintPreviewWidget(parent.printer)
        #Создаем панель предварительного просмотра (экземпляр класса
        # QPrintPreviewWidget) и связываем его сигнал paintRequested с методом
        # print() компонента поля судоку, иначе эта панель ничего не выведет.
        self.ppw.paintRequested.connect(parent.sudoku.print)
        hBox2.addWidget(self.ppw)
        #Создав панель предварительного просмотра, связываем с ее методами
        # zoomIn() и zoomOut() сигналы clicked кнопок увеличения и уменьшения
        # масштаба
        btnZoomIn.clicked.connect(self.ppw.zoomIn)
        btnZoomOut.clicked.connect(self.ppw.zoomOut)
        #Создаем контейнер для кнопок, которые обычно выводятся в диалоговом
        # окне, добавляем в него кнопку закрытия и располагаем по вертикали
        box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Close, QtCore.Qt.Vertical)
        #Получаем только что созданную в контейнере кнопку, задаем для нее надпись
        # Закрыть, увеличенные размеры и связываем ее сигнал clicked с методом
        # accept(), унаследованным нашим диалоговым окном от класса Dialog.
        btnClose = box.button(QtWidgets.QDialogButtonBox.Close)
        btnClose.setText("&Закрыть")
        btnClose.setFixedSize(96, 64)
        btnClose.clicked.connect(self.accept)
        #Добавляем контейнер с кнопками во второй горизонтальный контейнер,
        # указав выравнивание по правой и верхней границам, т. е. расположение
        # в верхнем правом углу
        hBox2.addWidget(box,
                        alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        #Добавляем второй горизонтальный контейнер в вертикальный контейнер
        # и помещаем последний в окно
        vBox.addLayout(hBox2)
        self.setLayout(vBox)
        self.zoomReset() #Указываем масштаб по умолчанию — 1:1, вызвав метод zoomReset() окна

    def zoomReset(self):
        self.ppw.setZoomFactor(1)

