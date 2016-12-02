class Updater():
    def __init__(self):
        self.__current_version = "v0.0.3"
        self.latest_url = None
        self.is_latest = True

    def check_for_updates(self):
        # check github url https://api.github.com/repos/kjstouffer/python-vrops-api-tool/releases/latest
        # if can't connect, return.
        # set latest_url to response['html_url']
        # if response['tag_name'] > __current_version, then set is_latest to False.
