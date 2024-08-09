from PyQt5 import QtCore, QtWidgets
import sqlite3
from dialog_2 import Ui_DialogAdd

class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog, table_name):
        self.table_name = table_name

        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 120, 751, 291))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.cellChanged.connect(self.add_change)

        self.pushButtonSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonSave.setGeometry(QtCore.QRect(410, 80, 81, 41))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.pushButtonSave.clicked.connect(self.save_changes)

        self.pushButtonReset = QtWidgets.QPushButton(Dialog)
        self.pushButtonReset.setGeometry(QtCore.QRect(590, 80, 81, 41))
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.pushButtonReset.clicked.connect(self.reset_table)

        self.pushButtonAdd = DoubleClickButton(Dialog)
        self.pushButtonAdd.setGeometry(QtCore.QRect(500, 80, 81, 41))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonAdd.setText("Add")
        self.pushButtonAdd.doubleClicked.connect(self.add_row_dialog)

        self.pushButtonDelete = QtWidgets.QPushButton(Dialog)
        self.pushButtonDelete.setGeometry(QtCore.QRect(680, 80, 81, 41))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonDelete.clicked.connect(self.delete_row)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(13, 428, 751, 91))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlaceholderText('Статус сохранения.')
        self.plainTextEdit.setReadOnly(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.connect = sqlite3.connect('warehouse.db')
        self.dict_changes = {}
        self.columns_list = []
        self.last_id = 0
        self.load_table_data()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonSave.setText(_translate("Dialog", "Save"))
        self.pushButtonReset.setText(_translate("Dialog", "Reset"))
        self.pushButtonAdd.setText(_translate("Dialog", "Add"))
        self.pushButtonDelete.setText(_translate("Dialog", "Delete"))

    def load_table_data(self):
        self.dict_changes = {}
        with self.connect:
            resp = self.connect.execute(f"PRAGMA table_info({self.table_name})").fetchall()
            self.columns_list = [el[1] for el in resp]
            table_data = self.connect.execute(f"SELECT * FROM {self.table_name}").fetchall()
            rows_list = [str(el[0]) for el in table_data]

            self.tableWidget.setColumnCount(len(self.columns_list))
            self.tableWidget.setHorizontalHeaderLabels(self.columns_list)
            self.tableWidget.setRowCount(len(rows_list))

            for el, row_data in enumerate(table_data):
                for i, cell_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(cell_data))
                    if i == 0:
                        self.dict_changes[str(cell_data)] = {}
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                        if not self.last_id or cell_data > self.last_id:
                            self.last_id = cell_data
                    self.tableWidget.setItem(el, i, item)

    def add_row_dialog(self):
        dialog_add = QtWidgets.QDialog()
        ui_add = Ui_DialogAdd()
        ui_add.setupUi(dialog_add, self.columns_list)
        ui_add.table_name = self.table_name
        dialog_add.exec_()
        if ui_add.new_row:
            self.last_id += 1
            new_row = [str(self.last_id)] + ui_add.new_row
            self.dict_changes[str(self.last_id)] = dict(zip(self.columns_list, new_row))
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for i, cell_data in enumerate(new_row):
                item = QtWidgets.QTableWidgetItem(cell_data)
                if i == 0:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(row_position, i, item)

    def delete_row(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            return
        row_id = self.tableWidget.item(row, 0).text()
        self.tableWidget.removeRow(row)
        self.dict_changes[row_id] = None

    def add_change(self, row: int, column: int):
        unique_id = self.tableWidget.item(row, 0).text()
        new_value = self.tableWidget.item(row, column).text()
        column_name = self.tableWidget.horizontalHeaderItem(column).text()
        if unique_id in self.dict_changes:
            self.dict_changes[unique_id][column_name] = new_value

    def save_changes(self):
        try:
            with self.connect:
                self.connect.execute('BEGIN')
                for row_id, changes in self.dict_changes.items():
                    if changes is None:
                        self.connect.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (row_id,))
                    elif changes:
                        sql_insert = f"""INSERT OR REPLACE INTO {self.table_name} 
                                        ({', '.join(self.columns_list)})
                                        VALUES ({', '.join('?' * len(changes))})"""
                        self.connect.execute(sql_insert, list(changes.values()))
                self.connect.execute('COMMIT')
                self.plainTextEdit.setPlainText('Сохранение выполнено успешно.')
        except sqlite3.Error as err:
            self.connect.execute('ROLLBACK')
            self.plainTextEdit.setPlainText(f'Ошибка сохранения: {err}')

    def reset_table(self):
        self.load_table_data()

class DoubleClickButton(QtWidgets.QPushButton):
    doubleClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(DoubleClickButton, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.doubleClicked.emit()
        else:
            super(DoubleClickButton, self).mouseDoubleClickEvent(event)
