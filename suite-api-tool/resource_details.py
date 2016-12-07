from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from metrics_table import MetricsTable
from parent_child_table import ParentChildTable


class ResourceDetails(QWidget):
    def __init__(self,
                 parent,
                 clipboard,
                 metrics,
                 properties,
                 parents,
                 children):
        super().__init__(parent)
        self.clipboard = clipboard
        self.metrics_table = MetricsTable(self.clipboard)
        self.properties_table = MetricsTable(self.clipboard)
        self.parents_table = ParentChildTable(self.clipboard)
        self.children_table = ParentChildTable(self.clipboard)
        self.initUI(metrics, properties, parents, children)

    def initUI(self, metrics, properties, parents, children):
        hbox = QHBoxLayout()
        hbox.addLayout(self.__metric_property_view(metrics, properties))
        hbox.addLayout(self.__parent_child_views(parents, children))
        self.setLayout(hbox)

    def __parent_child_views(self, parents, children):
        vbox = QVBoxLayout()
        parents_label = QLabel()
        parents_label.setText("Parents: ")
        self.parents_table.reInit()
        self.parents_table.addResources(parents)
        children_label = QLabel()
        children_label.setText("Children: ")
        self.children_table.reInit()
        self.children_table.addResources(children)
        vbox.addWidget(parents_label)
        vbox.addWidget(self.parents_table)
        vbox.addWidget(children_label)
        vbox.addWidget(self.children_table)
        return vbox

    def __metric_property_view(self, metrics, properties):
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
        return vbox
