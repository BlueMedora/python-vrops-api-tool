import sys
from os.path import isfile
from client import Client
from resource_table import ResourceTable
from resource_details import ParentChildTable
from resource_details import ResourceDetails
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from updater import Updater
import json
import os
import webbrowser


class ToolUI(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        self.resize(800, 600)
        self.clipboard = clipboard
        self.__address_bar = QLineEdit()
        self.__adapter_type_combobox = QComboBox()
        self.__adapter_instance_combobox = QComboBox()
        self.__connect_button = QPushButton()
        self.__connect_button.setAutoDefault(True)
        self.__connection_label = QLabel()
        self.__resource_table = ResourceTable(clipboard)
        self.__resource_table.doubleClicked.connect(self.getResourceDetails)
        self.__client = None
        self.initUI()
        self.__check_for_updates()

    def initUI(self):
        self.__main_widget = QWidget()
        self.__main_widget.setLayout(self.__createMainLayout())
        self.setCentralWidget(self.__main_widget)
        self.__assignClickActions()
        self.setTabOrder(self.__address_bar, self.__connect_button)
        self.setTabOrder(self.__connect_button, self.__adapter_type_combobox)
        self.setTabOrder(
            self.__adapter_type_combobox, self.__resource_kind_combobox)
        self.setTabOrder(
            self.__resource_kind_combobox, self.__adapter_instance_combobox)
        self.setTabOrder(
            self.__adapter_instance_combobox, self.__resource_table)
        self.show()

    def __createMainLayout(self):
        vbox = QVBoxLayout()
        vbox.addLayout(self.__createAddressBar())
        vbox.addWidget(self.__connection_label)
        vbox.addLayout(self.__createAdapterKindSelector())
        vbox.addLayout(self.__createResourceKindSelector())
        vbox.addLayout(self.__createAdapterInstanceSelector())
        vbox.addWidget(self.__resource_table)
        return vbox

    def __createAddressBar(self):
        address_bar_layout = QHBoxLayout()
        address_bar_label = QLabel()
        address_bar_label.setText("Hostname:")
        self.__address_bar.setCompleter(
            QCompleter(self.__getCompleterListFromFile()))
        self.__connect_button.setText("Connect!")
        address_bar_layout.addWidget(address_bar_label)
        address_bar_layout.addWidget(self.__address_bar)
        address_bar_layout.addWidget(self.__connect_button)
        return address_bar_layout

    def __getCompleterListFromFile(self):
        if not isfile(os.path.join(
                      os.path.expanduser('~'),
                      ".config/suite-api-tool/completion_list")):
            return list()
        with open(os.path.join(
                  os.path.expanduser('~'),
                  ".config/suite-api-tool/completion_list"),
                  "r+") as f:
            lines = f.read().splitlines()
        return lines

    def __createAdapterKindSelector(self):
        adapter_kind_selector_layout = QHBoxLayout()
        label = QLabel("Adapter Type: ")
        self.__adapter_type_combobox.setFixedSize(500, 25)
        self.__adapter_type_combobox.activated.connect(
            self.__adapterKindComboBoxSelection)
        adapter_kind_selector_layout.addWidget(label)
        adapter_kind_selector_layout.addWidget(self.__adapter_type_combobox)
        return adapter_kind_selector_layout

    def __createResourceKindSelector(self):
        resource_kind_selector_layout = QHBoxLayout()
        label = QLabel("Resource Kind: ")
        self.__resource_kind_combobox = QComboBox()
        self.__resource_kind_combobox.setFixedSize(500, 25)
        self.__resource_kind_combobox.activated.connect(
            self.__adapterInstanceComboBoxSelection)
        resource_kind_selector_layout.addWidget(label)
        resource_kind_selector_layout.addWidget(self.__resource_kind_combobox)
        return resource_kind_selector_layout

    def __createAdapterInstanceSelector(self):
        adapter_instance_selector_layout = QHBoxLayout()
        label = QLabel("Adapter Instance: ")
        self.__adapter_instance_combobox.setFixedSize(500, 25)
        self.__adapter_instance_combobox.activated.connect(
            self.__adapterInstanceComboBoxSelection)
        adapter_instance_selector_layout.addWidget(label)
        adapter_instance_selector_layout.addWidget(
            self.__adapter_instance_combobox)
        return adapter_instance_selector_layout

    def __assignClickActions(self):
        self.__connect_button.clicked.connect(self.__connectClicked)

    def __connectClicked(self):
        try:
            user = self.__load_user_json()
            self.__client = Client(self.__address_bar.text(),
                                   user['username'], user['password'])
            self.__connection_label.setText("Currently Connected to: " +
                                            self.__address_bar.text())
        except ValueError as error:
            QMessageBox.warning(self.__main_widget,
                                "Warning", str(error), QMessageBox.Ok)
            return
        try:
            items = self.__client.getAdapterKinds()
            self.__address_bar.completer()
            self.__addItemsToAdapterKinds(items)
            self.__addItemToCompletionList(self.__address_bar.text())
            self.__address_bar.setCompleter(
                QCompleter(self.__getCompleterListFromFile()))
            self.__adapter_instance_combobox.clear()
            self.__resource_kind_combobox.clear()
        except Exception as error:
            QMessageBox.warning(self.__main_widget,
                                "Warning", str(error), QMessageBox.Ok)

    def __addItemsToAdapterKinds(self, items):
        self.__adapter_type_combobox.clear()
        for item in items:
            self.__adapter_type_combobox.addItem(item[0], item[1])

    def __addItemToCompletionList(self, item):
        current_list = list()
        if isfile(os.path.join(os.path.expanduser('~'),
                  ".config/suite-api-tool/completion_list")):
            with open(os.path.join(os.path.expanduser('~'),
                      ".config/suite-api-tool/completion_list"), "r+") as f:
                current_list = f.read().splitlines()
        if(item in current_list):
            current_list.remove(item)
        current_list.insert(0, item)
        with open(os.path.join(os.path.expanduser('~'),
                  ".config/suite-api-tool/completion_list"), 'w+') as file:
            file.write("\n".join(current_list))

    def __adapterKindComboBoxSelection(self):
        adapter_kind = self.__adapter_type_combobox.currentData()
        adapter_instances = self.__client.getAdapterInstances(adapter_kind)
        resource_kinds = self.__client.getResourceKindsByAdapterKind(
            adapter_kind)
        self.__addItemsToAdapterInstances(adapter_instances)
        self.__addItemsToResourceKinds(resource_kinds)

    def __addItemsToAdapterInstances(self, items):
        self.__adapter_instance_combobox.clear()
        for item in items:
            self.__adapter_instance_combobox.addItem(item[0], item[1])

    def __adapterInstanceComboBoxSelection(self):
        adapter_instance_id = self.__adapter_instance_combobox.currentData()
        resource_kind_id = self.__resource_kind_combobox.currentData()
        resources = self.__client.getResources(adapter_instance_id,
                                               resource_kind_id)
        self.__createResourceTable(resources)

    def __addItemsToResourceKinds(self, resource_kinds):
        self.__resource_kind_combobox.clear()
        for resource_kind in resource_kinds:
            self.__resource_kind_combobox.addItem(resource_kind[0],
                                                  resource_kind[1])

    def __createResourceTable(self, resources):
        self.__resource_table.setColumnCount(0)
        self.__resource_table.setRowCount(0)
        self.__resource_table.reInit()
        self.__resource_table.addResources(resources)

    def __load_user_json(self):
        if not os.path.isfile(os.path.join(
                os.path.expanduser('~'),
                '.config/suite-api-tool/user.json')):
            return {'username': 'admin', 'password': 'P@ssw0rd1'}

        with open(os.path.join(
                os.path.expanduser('~'),
                '.config/suite-api-tool/user.json'), 'r') as user_file:
            return json.load(user_file)

    def getResourceDetails(self):
        table = self.sender()
        if not (ResourceTable != type(table) or ParentChildTable != type(table)):
            return
        selected_items = table.selectedItems()
        all_same = all(e.row() == selected_items[0].row()
                       for e in selected_items)
        if not all_same:
            QMessageBox.warning(
                self.__main_widget, "Warning",
                "Please only select one row.", QMessageBox.Ok)
            return
        # get uuid of row
        resource_id = None
        resource_name = None
        for item in table.selectedItems():
            if item.column() == 0:
                resource_name = item.text()
            if item.column() == 1:
                resource_id = item.text()
        if resource_id is None or resource_name is None:
            QMessageBox.warning(
                self.__main_widget, "Warning",
                "Could not find one or both " +
                "of Name or UUID of resource selected.",
                QMessageBox.Ok)
            return
        metrics = self.__client.getMetricsByResourceUUID(resource_id)
        properties = self.__client.getPropertiesByResourceUUID(resource_id)
        children = self.__client.getChildResources(resource_id)
        parents = self.__client.getParentResources(resource_id)
        resource_details = ResourceDetails(
            self, self.clipboard, metrics, properties, children, parents)
        resource_details.children_table.doubleClicked.connect(self.getResourceDetails)
        resource_details.parents_table.doubleClicked.connect(self.getResourceDetails)
        resource_details.setWindowTitle(resource_name)
        resource_details.setWindowFlags(QtCore.Qt.Window)
        resource_details.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        resource_details.resize(800, 800)
        resource_details.show()

    def __check_for_updates(self):
        updater = Updater()
        updater.check_for_updates()
        if not updater.is_latest:
            response = QMessageBox.question(
                self.__main_widget, "Update Available!",
                "A New version of this tool is available," +
                " would you like to download it now?",
                (QMessageBox.Yes | QMessageBox.No))
            if response == QMessageBox.Yes:
                webbrowser.open(updater.latest_url)


if __name__ == '__main__':
    if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.config')):
        os.mkdir(os.path.join(os.path.expanduser('~'), '.config'), 0o644)
    if not os.path.isdir(os.path.join(os.path.expanduser('~'),
                                      '.config/suite-api-tool')):
        os.mkdir(os.path.join(os.path.expanduser('~'),
                              '.config/suite-api-tool'), 0o755)
    if not os.path.isfile(os.path.join(os.path.expanduser('~'),
                          '.config/suite-api-tool/completion_list')):
        open(os.path.join(
             os.path.expanduser('~'),
             '.config/suite-api-tool/completion_list'), 'a').close()
    if not os.path.isfile(os.path.join(os.path.expanduser('~'),
                          '.config/suite-api-tool/user.json')):
        user_dictionary = {'username': 'admin', 'password': 'P@ssw0rd1'}
        with open(os.path.join(
                  os.path.expanduser('~'),
                  '.config/suite-api-tool/user.json'),
                  'a') as default_file:
            json.dump(obj=user_dictionary, fp=default_file, indent=2)
    app = QApplication(sys.argv)
    ex = ToolUI(app.clipboard())
    sys.exit(app.exec_())
