from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class ResourceTable(QTableWidget):
    def __init__(self):
        super().__init__()

    def reInit(self):
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setColumnCount(2)
        headers = list()
        headers.append("Resource Name")
        headers.append("Resource UUID")
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
        row_count = self.rowCount()

        resource_name = QTableWidgetItem()

        resource_name.setText(resource['name'])
        self.setItem(row_index, 0, resource_name)
        uuid = QTableWidgetItem()
        uuid.setText(resource['uuid'])
        self.setItem(row_index, 1, uuid)

        for i, identifier in enumerate(resource['identifiers']):
            column_count = i+3
            column_index = i+2
            identifier_widget = QTableWidgetItem()
            identifier_widget.setText(identifier['value'])
            if self.columnCount() < column_count:
                header = QTableWidgetItem()
                header.setText(identifier['name'])
                self.setColumnCount(column_count)
                self.setHorizontalHeaderItem(column_index, header)
            self.setItem(row_index, column_index, identifier_widget)
