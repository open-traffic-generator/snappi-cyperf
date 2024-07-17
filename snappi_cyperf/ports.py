import ipaddress
import json
import re
import time
from snappi_cyperf.timer import Timer


class port(object):
    """
    Args
    ----
    - Cyperfapi (Api): instance of the Api class

    """

    def __init__(self, cyperfapi):
        self._api = cyperfapi

    def config(self, rest):
        """T"""
        self._config = self._api._l47config
        with Timer(self._api, "Port Configuration"):
            port_config = self._config.ports
            for port in port_config:
                if self._is_valid_ip(port.location):
                    self._assign_agents_by_ip(
                        rest, port.location, self._api._network_segments[port.name]
                    )
                else:
                    self._assign_agents_by_tag(
                        rest, port.location, self._api._network_segments[port.name]
                    )

            # rest.assign_agents()
            # rest.assign_agents_by_tag("user:port1", 1)
            # rest.assign_agents_by_ip("10.39.44.120", 1)
            # get_agents = rest.get_agents()
            # print("get_agents : ", get_agents)
            # self._create_chassis(rest)

    def _is_valid_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def _assign_agents_by_ip(self, rest, location, network_segment):
        rest.assign_agents_by_ip(location, network_segment)

    def _assign_agents_by_tag(self, rest, location, network_segment):
        rest.assign_agents_by_tag(location, network_segment)

    # def _create_chassis(self, rest):
    #     """Add any scenarios to the api server that do not already exist"""
    #     for device in self._config.devices:
    #         ethernet = device.ethernets[0]
    #         location = self._get_chasiss(
    #             ethernet.connection.port_name, self._config.ports
    #         )
    #         self._add_chassis(location)
    #         for ip in ethernet.ipv4_addresses:
    #             self._assign_ports(location, ip.name)

    # def _get_chasiss(self, port_name, port_config):
    #     """ """
    #     for port in port_config:
    #         if port.name == port_name:
    #             return port.location

    # def _add_chassis(self, location):
    #     """ """
    #     #
    #     chassis_name = location.split("/")[0]
    #     chassis_list_url = "%s/cyperf/chassisChain/chassisList" % (self._api._cyperf)
    #     payload = {"name": chassis_name}
    #     response = self._api._request("POST", chassis_list_url, payload)
    #     refresh_connection_url = "%s/%s/operations/refreshConnection" % (
    #         chassis_list_url,
    #         response,
    #     )
    #     response = self._api._request("POST", refresh_connection_url, {})
    #     time.sleep(10)
    #     # self._api._wait_for_action_to_finish(response, refresh_connection_url)

    # def _assign_ports(self, location, ip_name):
    #     """ """
    #     try:
    #         active_test_url = "%s/cyperf/test/activeTest" % (self._api._cyperf)
    #         payload = {"enableForceOwnership": "true"}
    #         response = self._api._request("PATCH", active_test_url, payload)
    #         url = self._api._config_url.get(ip_name)
    #         url = self._api.common.get_community_url(url)
    #         port_list_url = url + "network/portList"
    #         chassis_id = 1
    #         chassis_ip, card_id, port_id = location.split("/")
    #         payload = {"chassisId": chassis_id, "cardId": card_id, "portId": port_id}

    #         response = self._api._request("POST", port_list_url, payload)
    #     except Exception as err:
    #         # self.logger.info(f"error:{err}")
    #         raise Exception(str(err))
