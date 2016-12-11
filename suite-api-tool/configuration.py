from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
import os
import json
from collections import OrderedDict

class Configuration(QWidget):
    def __init__(self):
        super(Configuration, self).__init__()
        self.parameters = OrderedDict()
        self.parameters['ConfigurationName'] = None
        self.parameters['Username'] = None
        self.parameters['Password'] = None
        self.parameters['Hostname'] = None
        self.user_home_dir = '~'
        self.configuration_file_location = '.config/suite-api-tool/hosts.json'
        self.all_configurations = None
        self.create_ui()

    def create_ui(self):
        self.setLayout(self.__create_layout())
        self.show()
        return

    def __create_layout(self):
        vbox = QVBoxLayout()
        for field in self.parameters:
            hbox = QHBoxLayout()
            label = QLabel()
            label.setText(str(field)+":")
            hbox.addWidget(label)
            text_field = QLineEdit()
            text_field.setProperty("name",field)
            text_field.textChanged.connect(self.__field_changed)
            hbox.addWidget(text_field)
            vbox.addLayout(hbox)
        return vbox

    def __field_changed(self):
        field = self.sender()
        name = field.property("name")
        self.parameters[name] = field.text()

    def save_configuration(self):
        with open(os.path.join(
                    os.path.expanduser(self.user_home_dir),
                    self.configuration_file_location)) as config:
            json.dump(obj=self.all_configurations, fp=config, indent=2)
        return

    def load_all_configuration(self):
        if not os.path.isfile(
                os.path.join(
                    os.path.expanduser(self.user_home_dir),
                    self.configuration_file_location)):
            open(os.path.join(
                    os.path.expanduser(self.user_home_dir),
                    self.configuration_file_location), 'a').close()

        with open(os.path.join(
                    os.path.expanduser(self.user_home_dir),
                    self.configuration_file_location)) as config:
            self.loaded_configuration = json.load(config)
        return

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    config = Configuration()
    sys.exit(app.exec_())
    
