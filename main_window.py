from PyQt5 import QtCore, QtWidgets
from dialog_1 import Ui_Dialog
from functools import partial

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(32, 100, 151, 101))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 100, 151, 101))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(420, 100, 151, 101))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(610, 100, 151, 101))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(32, 290, 151, 101))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(230, 290, 151, 101))
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(420, 290, 151, 101))
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(610, 290, 151, 101))
        self.pushButton_8.setObjectName("pushButton_8")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Client"))
        self.pushButton_2.setText(_translate("MainWindow", "Position"))
        self.pushButton_3.setText(_translate("MainWindow", "Worker"))
        self.pushButton_4.setText(_translate("MainWindow", "Operation"))
        self.pushButton_5.setText(_translate("MainWindow", "Warehouse"))
        self.pushButton_6.setText(_translate("MainWindow", "Current_product"))
        self.pushButton_7.setText(_translate("MainWindow", "Product_property"))
        self.pushButton_8.setText(_translate("MainWindow", "Operation_product"))

        self.pushButton.clicked.connect(partial(self.dialog, "Client"))
        self.pushButton_2.clicked.connect(partial(self.dialog, "Position"))
        self.pushButton_3.clicked.connect(partial(self.dialog, "Worker"))
        self.pushButton_4.clicked.connect(partial(self.dialog, "Operation"))
        self.pushButton_5.clicked.connect(partial(self.dialog, "Warehouse"))
        self.pushButton_6.clicked.connect(partial(self.dialog, "Current_product"))
        self.pushButton_7.clicked.connect(partial(self.dialog, "Product_property"))
        self.pushButton_8.clicked.connect(partial(self.dialog, "Operation_product"))

    def dialog(self, table_name):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.setupUi(Dialog, table_name)
        # Dialog.show()
        Dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
