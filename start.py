from PyQt5 import QtGui, QtWidgets
import sys
from modules.mainwindow import MainWindow


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(r"images/svd.png"))
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Здесь мы создаем экземпляр класса QApplication, представляющий приложение,
# указываем для него значок, подготовленный ранее, создаем экземпляр только
# что написанного класса MainWindow, представляющего основное окно,
# выводим окно на экран и запускаем приложение.