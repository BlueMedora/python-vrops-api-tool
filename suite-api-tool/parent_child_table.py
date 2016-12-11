from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from easy_table import EasyTable


class ParentChildTable(EasyTable):
    def __init__(self, clipboard):
        super(ParentChildTable, self).__init__(clipboard)

    def reInit(self):
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setColumnCount(4)
        headers = list()
        headers.append("Resource Name")
        headers.append("Resource UUID")
        headers.append("Resource Type")
        headers.append("Adapter Kind")
        for i, header in enumerate(headers):
            header_item = QTableWidgetItem()
            header_item.setText(header)
            self.setHorizontalHeaderItem(i, header_item)

    def addResources(self, resources):
        for resource in resources:
            self.addResource(resource)
        self.resizeColumnsToContents()

    def addResource(self, resource):
        row_index = self.rowCount()
        self.insertRow(self.rowCount())

        resource_name = QTableWidgetItem()
        resource_name.setText(resource['name'])
        self.setItem(row_index, 0, resource_name)

        uuid = QTableWidgetItem()
        uuid.setText(resource['uuid'])
        self.setItem(row_index, 1, uuid)

        resource_type = QTableWidgetItem()
        resource_type.setText(resource['type'])
        self.setItem(row_index, 2, resource_type)

        adapter_type = QTableWidgetItem()
        adapter_type.setText(resource['adapter'])
        self.setItem(row_index, 3, adapter_type)
