from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from easy_table import EasyTable
class MetricsTable(EasyTable):
    def __init__(self, clipboard):
        super(MetricsTable, self).__init__(clipboard)
        self.reInit()

    def reInit(self):
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setColumnCount(2)
        headers = list()
        headers.append("Name")
        headers.append("Value")
        for i, header in enumerate(headers):
            header_item = QTableWidgetItem()
            header_item.setText(header)
            self.setHorizontalHeaderItem(i, header_item)

    def addMetrics(self, metrics):
        for metric in metrics:
            self.addMetric(metric)
        self.resizeColumnsToContents()

    def addMetric(self, metric):
        row_index = self.rowCount()
        self.insertRow(self.rowCount())

        metric_name = QTableWidgetItem()
        metric_value = QTableWidgetItem()
        metric_timestamp = QTableWidgetItem()

        metric_name.setText(metric['key'])
        metric_value.setText(str(metric.get('value', '')))
        self.setItem(row_index, 0, metric_name)
        self.setItem(row_index, 1, metric_value)

        if(metric.get('timestamp', None) is not None):
            if self.columnCount() < 3:
                self.setColumnCount(3)
                timestamp_header = QTableWidgetItem()
                timestamp_header.setText("Timestamp")
                self.setHorizontalHeaderItem(2, timestamp_header)
            metric_timestamp.setText(str(metric['timestamp']))
            self.setItem(row_index, 2, metric_timestamp)
