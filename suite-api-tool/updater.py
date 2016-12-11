import requests
import platform
from distutils.version import LooseVersion


class Updater():
    def __init__(self):
        self.__current_version = "v0.0.4"
        self.latest_url = None
        self.is_latest = True

    def check_for_updates(self):
        operating_system = platform.system()
        url = ("https://api.github.com/" +
               "repos/kjstouffer/python-vrops-api-tool/releases/latest")
        try:
            response = requests.get(url,
                                    headers={"Accept": "application/json"},
                                    timeout=5)
        except Exception:
            print("Unable to connect to github," +
                  " skip checking for latest version.")
            return

        json = response.json()

        if (LooseVersion(json['tag_name']) >
                LooseVersion(self.__current_version)):
            self.is_latest = False

        if self.is_latest:
            return

        if(operating_system == "Windows"):
            asset_filter = ".exe"
        elif(operating_system == "Darwin"):
            asset_filter = ".dmg"
        elif(operating_system == "Linux"):
            asset_filter = ".bin"
        else:
            return

        for asset in json['assets']:
            if asset_filter in asset['name']:
                self.latest_url = asset['browser_download_url']
                break
