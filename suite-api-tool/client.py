import requests
import re

class Client:

    def __init__(self, hostname):
        self.__username = 'admin'
        self.__password = 'P@ssw0rd1'
        if not self.is_valid_hostname(hostname):
            raise ValueError("Please enter a valid hostname!")
        self.__base_url = "https://"+hostname+"/suite-api/api"

    def getAdapterKinds(self):
        url = self.__base_url + "/adapterkinds"
        response = requests.get(url, auth=(self.__username, self.__password), headers={"Accept": "application/json"}, verify=False, timeout=5)
        keys = list()
        for thing in response.json()['adapter-kind']:
            keys.append((thing['name'], thing['key']))
        return keys

    def getAdapterInstances(self, adapter_kind):
        url = self.__base_url + "/adapters"
        payload = {"adapterKindKey": adapter_kind}
        response = requests.get(url,
                                auth=(self.__username, self.__password),
                                headers={"Accept": "application/json"},
                                params=payload,
                                verify=False,
                                timeout=5)
        keys = list()
        for thing in response.json()['adapterInstancesInfoDto']:
            keys.append((thing['resourceKey']['name'], thing['id']))
        return keys

    def getResources(self, adapter_instance_id):
        None

    def is_valid_hostname(self, hostname):
        if len(hostname) > 255:
            return False
        if len(hostname) <= 0:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

