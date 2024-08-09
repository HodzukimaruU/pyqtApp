from PyQt5 import QtCore, QtWidgets

class Ui_DialogAdd(QtWidgets.QDialog):
    def setupUi(self, Dialog, columns_list):
        self.columns_list = columns_list
        self.new_row = None

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 400)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.line_edits = []
        for i, column in enumerate(columns_list[1:], start=1):
            label = QtWidgets.QLabel(Dialog)
            label.setText(column)
            self.gridLayout.addWidget(label, i, 0)
            line_edit = QtWidgets.QLineEdit(Dialog)
            self.line_edits.append(line_edit)
            self.gridLayout.addWidget(line_edit, i, 1)

        self.pushButtonExecute = QtWidgets.QPushButton(Dialog)
        self.pushButtonExecute.setObjectName("pushButtonExecute")
        self.pushButtonExecute.setText("Execute")
        self.pushButtonExecute.clicked.connect(self.collect_data)
        self.gridLayout.addWidget(self.pushButtonExecute, len(columns_list), 0, 1, 2)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.plainTextEdit, len(columns_list) + 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add New Row"))

    def validate_data(self):
        column_types = {
            'Client': {'id': int, 'name': str, 'phone_number': int, 'json_note': str},
            'Current_product': {'id': int, 'quantity': int, 'operation_id': int, 'warehouse_id': int, 'delivery_date': int, 'expiration_date_operation': int},
            'Operation': {'id': int, 'type': str, 'client_id': int, 'worker_id': int, 'time': int, 'additional_characteristics': str},
            'Operation_product': {'id': int, 'operation_id': int, 'product_id': int, 'warehouse_id': int, 'quantity': int, 'condition': str},
            'Position': {'id': int, 'name_position': str, 'salary': int, 'access_level': int},
            'Product_property': {'id': int, 'current_product_id': int, 'current_product_name': str, 'category': str, 'characteristics': str, 'expiration_date': int, 'price': int, 'article_number': int, 'photo': bytes},
            'Warehouse': {'id': int, 'name': str, 'address': str, 'coordinates': int, 'geolocation': str, 'json_product': str},
            'Worker': {'id': int, 'name': str, 'birthday': int, 'phone_number': int, 'position_id': int, 'username': str, 'password': str}
        }

        table_column_types = column_types.get(self.table_name, {})
        for i, line_edit in enumerate(self.line_edits):
            column_name = self.columns_list[i + 1]
            expected_type = table_column_types.get(column_name)
            if expected_type:
                try:
                    value = line_edit.text()
                    if expected_type == int:
                        int(value)
                    elif expected_type == float:
                        float(value)
                    elif expected_type == bytes:
                        bytes(value, 'utf-8')
                    elif expected_type == str:
                        if value.isdigit():
                            raise ValueError("Ошибка")
                        str(value)
                except ValueError:
                    self.plainTextEdit.setPlainText(f"Ошибка добавления: неверный тип данных для {column_name}. Ожидается {expected_type.__name__}.")
                    return False
        return True

    def collect_data(self):
        if self.validate_data():
            self.new_row = [line_edit.text() for line_edit in self.line_edits]
            self.plainTextEdit.setPlainText("Успешно выполнено.")
            self.accept()
        else:
            self.new_row = None

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_DialogAdd()
    ui.setupUi(Dialog, ["ID", "name", "phone_number", "json_note"])
    ui.table_name = ['Client', 'Position','Worker', 'Operation', 'Warehouse', 'Current_product', 'Product_property', 'Operation_product']
    Dialog.show()
    sys.exit(app.exec_())
