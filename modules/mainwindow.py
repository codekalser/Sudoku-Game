# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
import re
# Импортируем класс поля судоку Widget из модуля widget.py
from modules.widget import Widget
from modules.previewdialog import PreviewDialog


class MainWindow(QtWidgets.QMainWindow):
    """основное окно приложения «Судоку»"""

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent,
                                       flags=QtCore.Qt.Window |
                                             QtCore.Qt.MSWindowsFixedSizeDialogHint)
        # флаг MSWindowsFixedSizeDialogHint, запрещающий изменение его размеров
        self.setWindowTitle("Sudoku Game")
        # Указываем для окна таблицу стилей, которая задаст представление
        # для следующих элементов управления:
        self.setStyleSheet("QFrame QPushButton"
                           " {font-size:10pt;font-family:Verdana;"
                           "color:black;font-weight:bold;}"
                           "MyLabel {font-size:14pt;font-family:Verdana;"
                           "border:1px solid #9AA6A7;}")
        self.settings = QtCore.QSettings('учебная сборка: Сергей Калашников '
                                         'на основе книги Прохоренок Н.А., Дронов В.А.'
                                         ' - Python 3 и PyQt 5. Разработка приложений'
                                         ' (Профессиональное программирование)'
                                         ' 2019', "Судоку")
        self.printer = QtPrintSupport.QPrinter()  # Создаем объекты хранилища настроек и принтера

        # Создаем экземпляр класса Widget, сохраняем его в атрибуте sudoku
        # и помещаем в окно в качестве центрального.
        self.sudoku = Widget()
        self.setCentralWidget(self.sudoku) #Чтобы создать SDI-приложение, следует с помощью метода
                                                        #setCentralWidget() класса QMainWindow установить компонент
                                                        # отображающий содержимое документа;
        menuBar = self.menuBar()  # Получаем доступ к уже имеющемуся в окне главному меню
        toolBar = QtWidgets.QToolBar()  # создаем панель инструментов.
        myMenuFile = menuBar.addMenu("&Файл")  # Создаем меню Файл
        action = myMenuFile.addAction(QtGui.QIcon(r"images/new.png"),  # название
                                      "&Новый", self.sudoku.onClearAllCells,  # обработчик
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_N)  # комибнация клавиш
        # формируется action (действие) (экземпляр класса QAction)
        # создается связанный с ним пункт меню
        # возвращается действие в качестве результата
        # сохраним полученное действие в переменной,
        # чтобы впоследствии создать на панели инструментов связанную с ним
        # кнопку и задать для него текст подсказки,
        # выводящийся в строке состояния.
        toolBar.addAction(action)
        action.setStatusTip("Новая игра")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/open.png"),
                                      "&Открыть...", self.onOpenFile,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        toolBar.addAction(action)
        action.setStatusTip("Загрузка головоломки из файла")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/save.png"),
                                      "Со&хранить...", self.onSave,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        toolBar.addAction(action)
        action.setStatusTip("Сохранение головоломки в файле")

        action = myMenuFile.addAction("&Сохранить компактно...",
                                      self.onSaveMini)
        action.setStatusTip(
            "Сохранение головоломки в компактном формате")
        myMenuFile.addSeparator()
        toolBar.addSeparator()

        action = myMenuFile.addAction(QtGui.QIcon(r"images/print.png"),
                                      "&Печать...", self.onPrint,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_P)
        toolBar.addAction(action)
        action.setStatusTip("Печать головоломки")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/preview.png"),
                                      "П&редварительный просмотр...",
                                      self.onPreview)
        toolBar.addAction(action)
        action.setStatusTip("Предварительный просмотр головоломки")

        action = myMenuFile.addAction("П&араметры страницы...",
                                      self.onPageSetup)
        action.setStatusTip("Задание параметров страницы")
        myMenuFile.addSeparator()  # Добавляем в меню и
        toolBar.addSeparator()  # на панель инструментов разделители

        action = myMenuFile.addAction("&Выход", QtWidgets.qApp.quit,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        action.setStatusTip("Выход")

        myMenuEdit = menuBar.addMenu("&Правка")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/copy.png"),
                                      "К&опировать", self.onCopyData,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        toolBar.addAction(action)
        action.setStatusTip("Копирование головоломки в буфер обмена")

        action = myMenuEdit.addAction("&Копировать компактно",
                                      self.onCopyDataMini)
        action.setStatusTip("Копирование в компактном формате")

        action = myMenuEdit.addAction("Копировать &для Excel",
                                      self.onCopyDataExcel)
        action.setStatusTip("Копирование в формате MS Excel")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/paste.png"),
                                      "&Вставить", self.onPasteData,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_V)
        toolBar.addAction(action)
        action.setStatusTip("Вставка головоломки из буфера обмена")

        action = myMenuEdit.addAction("Вставить &из Excel",
                                      self.onPasteDataExcel)
        action.setStatusTip("Вставка головоломки из MS Excel")
        myMenuEdit.addSeparator()
        toolBar.addSeparator() #

        action = myMenuEdit.addAction("&Блокировать",
                                      self.sudoku.onBlockCell, QtCore.Qt.Key_F2)
        action.setStatusTip("Блок активной ячейки")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/lock.png"),
                                      "Б&локировать все",
                                      self.sudoku.onBlockCells, QtCore.Qt.Key_F3)
        toolBar.addAction(action)
        action.setStatusTip("Блок всех ячеек")
        action = myMenuEdit.addAction("&Разблокировать",
                                      self.sudoku.onClearBlockCell,
                                      QtCore.Qt.Key_F4)
        action.setStatusTip("Разблок активной ячейки")
        action = myMenuEdit.addAction(QtGui.QIcon(r"images/unlock.png"),
                                      "Р&азблокировать все",
                                      self.sudoku.onClearBlockCells,
                                      QtCore.Qt.Key_F5)
        toolBar.addAction(action)
        action.setStatusTip("Разблокирование всех ячеек")

        myMenuAbout = menuBar.addMenu("&Справка")
        action = myMenuAbout.addAction("О &программе...", self.aboutInfo)
        action.setStatusTip("Получение сведений о приложении")
        action = myMenuAbout.addAction("О &Qt...", QtWidgets.qApp.aboutQt)
        action.setStatusTip("Получение сведений о библиотеке Qt")

        # Запрещаем панели инструментов перемещаться внутри области,
        # в которой она находится, и выноситься в отдельное окно
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)

        # Получаем доступ к строке состояния, убираем маркер изменения размера
        # выводим приветственное сообщение, которое будет отображаться 20 сек
        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("Welcome To The Sudoku Game", 20000)

        # Проверяем, находятся ли в хранилище настроек X и Y верхнего угла окна
        # если это так, извлекаем эти значения и позиц окно по этим коорд
        if self.settings.contains("X") and self.settings.contains("Y"):
            self.move(self.settings.value("X"), self.settings.value("Y"))

    # Метод closeEvent() будет автоматически вызван при закрытии окна.
    # В нем мы выполняем сохранение текущих координат
    # левого верхнего угла окна
    def closeEvent(self, evt):
        g = self.geometry()
        self.settings.setValue("X", g.left())
        self.settings.setValue("Y", g.top())

    def onCopyData(self):#помещает в буфер обмена результат
        QtWidgets.QApplication.clipboard().setText(
            self.sudoku.getDataAllCells())

    def onCopyDataMini(self): #помещает в буфер обмена результат
        QtWidgets.QApplication.clipboard().setText(
            self.sudoku.getDataAllCellsMini())

    def onCopyDataExcel(self):#помещает в буфер обмена результат
        QtWidgets.QApplication.clipboard().setText(
            self.sudoku.getDataAllCellsExcel())

    def onPasteData(self): #вставляет данные в полном или компактном формате
        data = QtWidgets.QApplication.clipboard().text()
        if data: #удостоверяется, что данные для вставки
                    # вообще есть (не равны пустой строке)
            if len(data) == 81 or len(data) == 162: # что их длина 81 или 162 симв
                r = re.compile(r"[^0-9]")
            if not r.match(data): #не присутствует ли в строке символ, отличный от цифр
                self.sudoku.setDataAllCells(data) #передается строка с данными для вставки
                return #выполняется выход из метода
        self.dataErrorMsg()

    def onPasteDataExcel(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            data = data.replace("\r", "") #удалим символы возврата каретки
            r = re.compile(r"([0-9]?[\t\n]){81}") #Полученная нами строка представляет собой набор из строго 81-й комбинации двух символов: цифры от 0...9, которая может присутствовать в единственном числе или отсутствовать, и символа табуляции или перевода строки.
            if r.match(data): #сравниваем с ним строку с данными и выполняем дальнейшие манипуляции, только если сравнение выполняется
                result = []
                if data[-1] == "\n": # Удаляем из полученной строки с данными завершающий символ перевода строки
                    data = data[:-1]
                dl = data.split("\n") #Разбиваем строку по символам перевода строки
                for sl in dl: #отдельные строки поля судоку
                    dli = sl.split("\t")
                    for sli in dli: #сведения об одной ячейке
                        if len(sli) == 0: #Если очередной элемент-строка пуст
                            result.append("00") #"00", где первая цифра обозначает, что ячейка не заблокирована, а вторая — отсутствие цифры в ячейке
                        else: #Если же элемент не пуст, значит, он представляет собой цифру
                            result.append("0" + sli[0]) #добавляем в список строку вида "0<Эта цифра>
                data = "".join(result)
                self.sudoku.setDataAllCells(data) #передаем строку методу setDataAllCells()
                return #выполняем возврат из метода
        self.dataErrorMsg() #сообщение о неправильном формате данных

    def dataErrorMsg(self):
        QtWidgets.QMessageBox.information(self, "Sudoku Game",
                                          "Данные имеют неправильный формат")

    def onOpenFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "Выберите файл",
                                                         QtCore.QDir.homePath(),
                                                         "Судоку (*.svd)")[0]
        if fileName:
            data = ""
            try:
                with open(fileName, newline="") as f:
                    data = f.read()
            except: #файл прочитать не удалось, и было сгенерировано исключение
                QtWidgets.QMessageBox.information(self, "Судоку",
                                                  "Не удалось открыть файл")
                return
            if len(data) > 2:
                if data[-1] == "\n":
                    data = data[:-1]
                if len(data) == 81 or len(data) == 162:
                    r = re.compile(r"[^0-9]")
                    if not r.match(data): #передаем загруженные данные все тому же
                        # методу setDataAllCells() класса поля судоку и выполняем возврат.
                        self.sudoku.setDataAllCells(data)
                        return
            self.dataErrorMsg()

    def onSave(self): #вызывают метод saveSVDFile() передав ему результат
                             # возвращенный методoм getDataAllCells()
        self.saveSVDFile(self.sudoku.getDataAllCells())

    def onSaveMini(self):
        self.saveSVDFile(self.sudoku.getDataAllCellsMini())

    def saveSVDFile(self, data):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "Выберите файл", QtCore.QDir.homePath(),
                                                         "Судоку (*.svd)")[0]
        if fileName:
            try:
                with open(fileName, mode="w", newline="") as f:
                    f.write(data)
                self.statusBar().showMessage("Файл сохранен", 10000)
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                                                  "Не удалось сохранить файл")

    def onPrint(self):
        pd = QtPrintSupport.QPrintDialog(self.printer, parent=self)
        pd.setOptions(QtPrintSupport.QAbstractPrintDialog.PrintToFile |
                      QtPrintSupport.QAbstractPrintDialog.PrintSelection)
        if pd.exec() == QtWidgets.QDialog.Accepted:
            self.sudoku.print(self.printer)

    def onPreview(self):
        pd = PreviewDialog(self)
        pd.exec()

    def onPageSetup(self):
        pd = QtPrintSupport.QPageSetupDialog(self.printer, parent=self)
        pd.exec()

    def aboutInfo(self):
        QtWidgets.QMessageBox.about(self, "О программе",
                                    "<center>Sudoku Game<br><br>"
                                    "Учебная версия - 2021 | Сергей Калашников <br><br>"
                                    "(c) Источник: Прохоренок Н.А., Дронов В.А. 2011-2018 гг.")
