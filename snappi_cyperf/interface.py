import json
import re
import time
from snappi_cyperf.timer import Timer


class interfaces(object):
    """Transforms OpenAPI objects into IxNetwork objects
    - Lag to /lag
    Args
    ----
    - cyperfapi (Api): instance of the Api class

    """

    _ETHERNET = {
        "mac": "MacStart",
        "step": "MacIncr",
        "count": "Count",
        "max_count": "maxCountPerAgent",
    }

    _IP = {
        "address": "IpStart",
        "gateway": "GwStart",
        "prefix": "NetMask",
        "name": "networkTags",
        "step": "IpIncr",
        "count": "Count",
        "max_count": "maxCountPerAgent",
    }

    _MTU_MSS = {
        "mtu": "Mss",
    }

    _VLAN = {
        "id": "VlanId",
        "step": "VlanIncr",
        "count": "Count",
        "per_count": "CountPerAgent",
        "priority": "Priority",
        "tpid": "TagProtocolId",
    }

    def __init__(self, cyperfapi):
        self._api = cyperfapi
        self._network_segment_cnt = 0
        self._ip_range_cnt = 0

    def config(self, rest):
        """T"""
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "Interface Configuration"):
            self._create_devices(rest)

    def _create_devices(self, rest):
        """Add any scenarios to the api server that do not already exist"""
        self._network_segment_cnt = 1
        for device in self._devices_config:
            self._create_ethernet(device, rest)

    def _create_ethernet(self, device, rest):
        """Add any scenarios to the api server that do not already exist"""
        for ethernet in device.ethernets:
            self._api._network_segments[ethernet.name] = self._network_segment_cnt
            self._api._network_segments[ethernet.connection.port_name] = (
                self._network_segment_cnt
            )
            self._network_segment_cnt = self._network_segment_cnt + 1
            payload = self._api._set_payload(ethernet, interfaces._ETHERNET)
            payload["MacAuto"] = False
            payload["OneMacPerIP"] = False
            rest.set_eth_range(
                payload,
                self._api._network_segments[ethernet.name],
            )
            self._create_ipv4(ethernet, rest)
        print("Network Segments - ", self._api._network_segments)

    def _create_ipv4(self, ethernet, rest):
        """
        Add any ipv4 to the api server that do not already exist
        """
        ipv4_addresses = ethernet.get("ipv4_addresses")
        if ipv4_addresses is None:
            return
        self._ip_range_cnt = 1
        for ipv4 in ethernet.ipv4_addresses:
            self._api._ip_ranges[ipv4.name] = self._ip_range_cnt
            self._ip_range_cnt = self._ip_range_cnt + 1
            payload = self._api._set_payload(ipv4, interfaces._IP)
            payload["IpAuto"] = False
            payload["NetMaskAuto"] = False
            payload["GwAuto"] = False
            payload.update(self._api._set_payload(ethernet, interfaces._MTU_MSS))
            mss = payload["Mss"]
            payload["Mss"] = mss - 28
            network_tag = payload["networkTags"]
            payload["networkTags"] = [network_tag]
            rest.set_ip_range(
                payload,
                self._api._network_segments[ethernet.name],
                self._api._ip_ranges[ipv4.name],
            )
            self._create_vlan(ethernet, ipv4, rest)

        print("Ip Ranges - ", self._api._ip_ranges)

    def _create_vlan(self, ethernet, ipv4, rest):
        """
        Add any ipv4 to the api server that do not already exist
        """
        vlans = ethernet.get("vlans")
        if vlans is None:
            return
        for vlan in ethernet.vlans:
            payload = self._api._set_payload(vlan, interfaces._VLAN)
            payload["VlanEnabled"] = True
            payload["TagProtocolId"] = 33024
            rest.set_ip_range_innervlan_range(
                payload,
                self._api._network_segments[ethernet.name],
                self._api._ip_ranges[ipv4.name],
            )
