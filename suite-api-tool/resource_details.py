from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from metrics_table import MetricsTable

class ResourceDetails(QWidget):

    def __init__(self, parent, clipboard, metrics, properties):
        super().__init__(parent)
        self.clipboard = clipboard
        self.metrics_table = MetricsTable(self.clipboard)
        self.properties_table = MetricsTable(self.clipboard)
        self.initUI(metrics, properties)

    def initUI(self, metrics, properties):
        vbox = QVBoxLayout()
        properties_label = QLabel()
        properties_label.setText("Properties: ")
        self.properties_table.addMetrics(properties)
        metrics_label = QLabel()
        metrics_label.setText("Metrics: ")
        self.metrics_table.addMetrics(metrics)
        vbox.addWidget(properties_label)
        vbox.addWidget(self.properties_table)
        vbox.addWidget(metrics_label)
        vbox.addWidget(self.metrics_table)
        self.setLayout(vbox)

