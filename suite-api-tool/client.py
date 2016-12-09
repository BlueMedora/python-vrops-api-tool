import requests
import re


class Client:

    def __init__(self, hostname, username, password):
        self.__username = username
        self.__password = password
        if not self.is_valid_hostname(hostname):
            raise ValueError("Please enter a valid hostname!")
        self.__base_url = "https://" + hostname + "/suite-api/api"
        self.adapter_kind = None
        self.resource_kinds = None

    def getAdapterKinds(self):
        url = self.__base_url + "/adapterkinds"
        response = requests.get(url,
                                auth=(self.__username, self.__password),
                                headers={"Accept": "application/json"},
                                verify=False,
                                timeout=5)
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
        endpoint = "/adapterkinds/" + adapter_kind + "/resourcekinds"
        json = self.__get(endpoint)
        resource_kinds = list()
        for resource_kind in json['resource-kind']:
            resource_kinds.append((resource_kind['name'],
                                   resource_kind['key']))
        resource_kinds = sorted(resource_kinds, key=lambda k: k[0].lower())
        return resource_kinds

    def getResources(self, adapter_instance_id, resource_kinds):
        resources = self.__getResourceList(adapter_instance_id, resource_kinds)
        return self.__processResources(resources)

    def getChildResources(self, resource_id):
        resources = self.__getChildResourceList(resource_id)
        return self.__processResources(resources)

    def __getChildResourceList(self, resource_id):
        page = 0
        resource_list = list()
        while True:
            endpoint = "/resources/" + resource_id + "/relationships/children"
            json_response = self.__get(endpoint)
            # add resources to list
            resource_list.extend(json_response["resourceList"])
            if self.__isLastPage(json_response['pageInfo']):
                break
            page += 1
        return resource_list

    def getParentResources(self, resource_id):
        resources = self.__getParentResourceList(resource_id)
        return self.__processResources(resources)

    def __getParentResourceList(self, resource_id):
        page = 0
        resource_list = list()
        while True:
            endpoint = "/resources/" + resource_id + "/relationships/parents"
            json_response = self.__get(endpoint)
            # add resources to list
            resource_list.extend(json_response["resourceList"])
            if self.__isLastPage(json_response['pageInfo']):
                break
            page += 1
        return resource_list

    def __getResourceList(self, adapter_instance_id, resource_kinds):
        page = 0
        resource_list = list()
        while True:
            payload = {"adapterInstanceId": adapter_instance_id,
                       "resourceKind": resource_kinds,
                       "page": page}
            json_response = self.__get("/resources", payload)
            # add resources to list
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
            resource_dict['adapter'] = resource[
                'resourceKey']['adapterKindKey']
            resource_dict['type'] = resource['resourceKey']['resourceKindKey']
            resource_dict['identifiers'] = list()
            resource_identifiers = resource[
                'resourceKey']['resourceIdentifiers']
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
        metric_response = self.__get(endpoint, payload)
        metrics = list()

        metric_units = self.getMetricUnitsByResourceUUID(uuid)

        for entry in metric_response.get('values', list()):
            for stat in entry['stat-list']['stat']:
                metric = dict()
                metric['key'] = stat['statKey']['key']
                metric['timestamp'] = stat['timestamps'][0]
                metric['value'] = stat['data'][0]
                metric['units'] = metric_units[metric['key']]
                metrics.append(metric)
        metrics = sorted(metrics, key=lambda k: k['key'].lower())
        return metrics

    def getMetricUnitsByResourceUUID(self, uuid):
        resource_kind_response = self.__get('/resources/' + str(uuid), list())
        resource_kind = resource_kind_response.get('resourceKey').get('resourceKindKey')
        adapter_kind = resource_kind_response.get('resourceKey').get('adapterKindKey')

        endpoint = "/adapterkinds/" + adapter_kind + "/resourcekinds/" + resource_kind + "/statkeys"
        metric_units_response = self.__get(endpoint, list())

        metric_units = dict()

        for metric in metric_units_response.get('resourceTypeAttributes'):
            key = metric.get('key')
            try:
                if metric.get('unit') is not None:
                    metric_units[key] = metric.get('unit')
                else:
                    metric_units[key] = '--'
            except:
                metric_units[key] = '--'
        return metric_units

    def getPropertiesByResourceUUID(self, uuid):
        endpoint = '/resources/' + str(uuid) + '/properties'
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
            # strip exactly one dot from the right, if present
            hostname = hostname[:-1]
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
