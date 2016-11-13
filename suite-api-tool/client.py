import requests
import re
class Client:

    def __init__(self, hostname):
        self.__username = 'admin'
        self.__password = 'P@ssw0rd1'
        if not self.is_valid_hostname(hostname):
            raise ValueError("Please enter a valid hostname!")
        self.__base_url = "https://"+hostname+"/suite-api/api"
        self.adapter_kind = None
        self.resource_kinds = None

    def getAdapterKinds(self):
        url = self.__base_url + "/adapterkinds"
        response = requests.get(url, auth=(self.__username, self.__password), headers={"Accept": "application/json"}, verify=False, timeout=5)
        keys = list()
        for thing in response.json()['adapter-kind']:
            keys.append((thing['name'], thing['key']))
        keys = sorted(keys, key=lambda k: k[0].lower())
        return keys

    def getAdapterInstances(self, adapter_kind):
        payload = {"adapterKindKey": adapter_kind}
        json = self.__get("/adapters", payload)
        keys = list()
        for thing in json['adapterInstancesInfoDto']:
            keys.append((thing['resourceKey']['name'], thing['id']))
        keys = sorted(keys, key=lambda k: k[0].lower())
        return keys

    def getResourceKindsByAdapterKind(self, adapter_kind):
        endpoint = "/adapterkinds/"+adapter_kind+"/resourcekinds"
        json = self.__get(endpoint)
        resource_kinds = list()
        for resource_kind in json['resource-kind']:
            resource_kinds.append((resource_kind['name'], resource_kind['key']))
        resource_kinds = sorted(resource_kinds, key=lambda k: k[0].lower())
        return resource_kinds

    def getResources(self, adapter_instance_id, resource_kinds):
        resources = self.__getResourceList(adapter_instance_id, resource_kinds)
        return self.__processResources(resources)

    def __getResourceList(self, adapter_instance_id, resource_kinds):
        page = 0
        resource_list = list()
        while True:
            url = self.__base_url + "/resources"
            payload = {"adapterInstanceId": adapter_instance_id, "resourceKind": resource_kinds, "page": page}
            json_response = self.__get("/resources", payload)

            #add resources to list
            resource_list.extend(json_response["resourceList"])
            if self.__isLastPage(json_response['pageInfo']):
                break
            page += 1
        return resource_list

    def __isLastPage(self, page_info):
        total_items = page_info['totalCount']
        page_size = page_info['pageSize']
        page_index = page_info['page']
        last_page_index = total_items // page_size
        return page_index >= last_page_index

    def __processResources(self, resources):
        all_resources = list()
        for resource in resources:
            resource_dict = dict()
            resource_dict['name'] = resource['resourceKey']['name']
            resource_dict['uuid'] = resource['identifier']
            resource_dict['identifiers'] = list()
            resource_identifiers = resource['resourceKey']['resourceIdentifiers']
            for id in resource_identifiers:
                identifier = dict()
                identifier['name'] = id['identifierType']['name']
                identifier['value'] = id['value']
                resource_dict['identifiers'].append(identifier)
            all_resources.append(resource_dict)
        all_resources = sorted(all_resources, key=lambda k: k['name'].lower())
        return all_resources

    def getMetricsByResourceUUID(self, uuid):
        endpoint = '/resources/stats/latest'
        payload = {"resourceId": uuid}
        response = self.__get(endpoint, payload)
        metrics = list()

        for entry in response.get('values', list()):
            for stat in entry['stat-list']['stat']:
                metric = dict()
                metric['key'] = stat['statKey']['key']
                metric['timestamp'] = stat['timestamps'][0]
                metric['value'] = stat['data'][0]
                metrics.append(metric)
        metrics = sorted(metrics, key=lambda k: k['key'].lower())
        return metrics

    def getPropertiesByResourceUUID(self, uuid):
        endpoint = '/resources/'+str(uuid)+'/properties'
        response = self.__get(endpoint)
        properties = list()
        for stat in response['property']:
            prop = dict()
            prop['key'] = stat['name']
            prop['value'] = stat['value']
            properties.append(prop)
        properties = sorted(properties, key=lambda k: k['key'].lower())
        return properties

    def __get(self, endpoint, parameters=None):
        url = self.__base_url + endpoint
        print(url)
        response = requests.get(url,
                                auth=(self.__username, self.__password),
                                headers={"Accept": "application/json"},
                                params=parameters,
                                verify=False,
                                timeout=5)
        return response.json()


    def is_valid_hostname(self, hostname):
        if len(hostname) > 255:
            return False
        if len(hostname) <= 0:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

