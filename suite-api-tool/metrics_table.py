from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from easy_table import EasyTable
import time


class MetricsTable(EasyTable):
    def __init__(self, clipboard):
        super(MetricsTable, self).__init__(clipboard)
        self.reInit()

    def reInit(self):
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setColumnCount(3)
        headers = list()
        headers.append("Name")
        headers.append("Value")
        headers.append("Units")
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
        metric_unit = QTableWidgetItem()
        metric_timestamp = QTableWidgetItem()

        metric_name.setText(metric['key'])
        metric_value.setText(str(metric.get('value', '')))
        metric_unit.setText(str(metric.get('units', '')))
        self.setItem(row_index, 0, metric_name)
        self.setItem(row_index, 1, metric_value)
        self.setItem(row_index, 2, metric_unit)

        if(metric.get('timestamp', None) is not None):
            if self.columnCount() < 4:
                self.setColumnCount(4)
                timestamp_header = QTableWidgetItem()
                timestamp_header.setText("Timestamp")
                self.setHorizontalHeaderItem(3, timestamp_header)
            timestamp = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(metric['timestamp'] / 1000))
            metric_timestamp.setText(timestamp)
            self.setItem(row_index, 3, metric_timestamp)
