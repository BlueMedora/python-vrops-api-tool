import sys
from client import Client
from PyQt5.QtWidgets import *

class ToolUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__address_bar = QLineEdit()
        self.__adapter_type_combobox = QComboBox
        self.__adapter_instance_combobox = QComboBox
        self.__connect_button = QPushButton
        self.__client = None
        self.initUI()

    def initUI(self):
        self.__main_widget = QWidget()
        self.__main_widget.setLayout(self.__createMainLayout())
        self.setCentralWidget(self.__main_widget)
        self.__assignClickActions()
        self.show()

    def __createMainLayout(self):
        vbox = QVBoxLayout()
        vbox.addLayout(self.__createAddressBar())
        vbox.addLayout(self.__createAdapterKindSelector())
        vbox.addLayout(self.__createAdapterInstanceSelector())
        return vbox

    def __createAddressBar(self):
        address_bar_layout = QHBoxLayout()
        address_bar_label = QLabel()
        address_bar_label.setText("Hostname:")
        self.__address_bar = QLineEdit()
        self.__address_bar.setCompleter(QCompleter(self.__getCompleterListFromFile()))
        self.__connect_button = QPushButton()
        self.__connect_button.setText("Connect!")
        address_bar_layout.addWidget(address_bar_label)
        address_bar_layout.addWidget(self.__address_bar)
        address_bar_layout.addWidget(self.__connect_button)
        return address_bar_layout

    def __getCompleterListFromFile(self):
        with open("completion_list") as f:
            lines = f.read().splitlines()
        return lines

    def __createAdapterKindSelector(self):
        adapter_kind_selector_layout = QHBoxLayout()
        label = QLabel("Adapter Type: ")
        self.__adapter_type_combobox = QComboBox()
        self.__adapter_type_combobox.setFixedSize(500,25)
        self.__adapter_type_combobox.activated.connect(self.__adapterKindComboBoxSelection)
        adapter_kind_selector_layout.addWidget(label)
        adapter_kind_selector_layout.addWidget(self.__adapter_type_combobox)
        return adapter_kind_selector_layout

    def __createAdapterInstanceSelector(self):
        adapter_instance_selector_layout = QHBoxLayout()
        label = QLabel("Adapter Instance: ")
        self.__adapter_instance_combobox = QComboBox()
        self.__adapter_instance_combobox.setFixedSize(500,25)
        self.__adapter_instance_combobox.activated.connect(self.__adapterInstanceComboBoxSelection)
        adapter_instance_selector_layout.addWidget(label)
        adapter_instance_selector_layout.addWidget(self.__adapter_instance_combobox)
        return adapter_instance_selector_layout

    def __assignClickActions(self):
        self.__connect_button.clicked.connect(self.__connectClicked)

    def __connectClicked(self):
        try:
            self.__client = Client(self.__address_bar.text())
        except ValueError as error:
            QMessageBox.warning(self.__main_widget, "Warning", str(error), QMessageBox.Ok)
            return
        try:
            items = self.__client.getAdapterKinds()
            self.__adapter_type_combobox.clear()
            self.__addItemsToAdapterKinds(items)
            self.__addItemToCompletionList(self.__address_bar.text())
            self.__address_bar.setCompleter(QCompleter(self.__getCompleterListFromFile()))
        except Exception as error:
            QMessageBox.warning(self.__main_widget, "Warning", str(error), QMessageBox.Ok)

    def __addItemsToAdapterKinds(self, items):
        for item in items:
            self.__adapter_type_combobox.addItem(item[0], item[1])

    def __addItemToCompletionList(self, item):
        with open("completion_list", 'a+') as file:
            file.write(item+"\n")

    def __adapterKindComboBoxSelection(self):
        adapter_kind = self.__adapter_type_combobox.currentData()
        adapter_instances = self.__client.getAdapterInstances(adapter_kind)
        self.__addItemsToAdapterInstances(adapter_instances)

    def __addItemsToAdapterInstances(self,items):
        for item in items:
            self.__adapter_instance_combobox.addItem(item[0], item[1])

    def __adapterInstanceComboBoxSelection(self):
        adapter_instance_id = self.__adapter_instance_combobox.currentData()
        self.__client.getResources(adapter_instance_id)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ToolUI()
    sys.exit(app.exec_())
