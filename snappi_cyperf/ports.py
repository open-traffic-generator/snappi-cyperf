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
