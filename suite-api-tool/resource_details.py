from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5 import QtCore
from metrics_table import MetricsTable
from parent_child_table import ParentChildTable


class ResourceDetails(QWidget):
    def __init__(self,
                 parent,
                 clipboard,
                 resource_information,
                 metrics,
                 properties,
                 parents,
                 children):
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.clipboard = clipboard
        self.metrics_table = MetricsTable(self.clipboard)
        self.properties_table = MetricsTable(self.clipboard)
        self.parents_table = ParentChildTable(self.clipboard)
        self.children_table = ParentChildTable(self.clipboard)
        self.initUI(resource_information, metrics, properties, parents, children)

    def initUI(self, resource_information, metrics, properties, parents, children):
        vbox = QVBoxLayout()
        vbox.addLayout(self.__resource_information_pane(resource_information))
        vbox.addLayout(self.__metrics_relationships_views(metrics, properties, parents, children))
        self.setLayout(vbox)

    def __resource_information_pane(self, resource_information):
        vbox = QVBoxLayout()
        for key, value in resource_information.items():
            hbox = QHBoxLayout()
            key_label = QLabel()
            key_label.setText(str(key) + ":")
            key_label.setAlignment(QtCore.Qt.AlignRight)
            hbox.addWidget(key_label)
            value_label = QLabel()
            value_label.setText(value)
            hbox.addWidget(value_label)
            vbox.addLayout(hbox)
        return vbox

    def __metrics_relationships_views(self, metrics, properties, parents, children):
        hbox = QHBoxLayout()
        hbox.addLayout(self.__metric_property_view(metrics, properties))
        hbox.addLayout(self.__parent_child_views(parents, children))
        return hbox

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

    def keyPressEvent(self, key_event):
        if (key_event.key() == QtCore.Qt.Key_W and
                key_event.modifiers().__eq__(QtCore.Qt.ControlModifier)):
            self.close()
