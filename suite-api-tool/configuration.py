from PyQt5.QtWidgets import QWidget
import os
import json

class Configuration(QWidget):
    def __init__(self):
        super(Configuration, self).__init__()
        self.username = None
        self.password = None
        self.hostname = None
        self.user_home_dir = '~'
        self.configuration_file_location = '.config/suite-api-tool/hosts.json'
        self.all_configurations = None

    def create_ui():
        return

    def save_configuration():
        with open(os.path.join(
                    os.path.expanduser(self.user_home_dir),
                    self.configuration_file_location)) as config:
            json.dump(obj=self.all_configurations, fp=config, indent=2)
        return

    def load_all_configuration():
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
