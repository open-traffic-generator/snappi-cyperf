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

    # def _create_devices(self):
    #     """Add any scenarios to the api server that do not already exist
    #     """
    #     for device in self._devices_config:
    #         url1 = self._api._ixload + "ixload/test/activeTest/communityList"
    #         payload = {}
    #         response = self._api._request('POST', url1, payload)
    #         new_url = url1 + "/" + response + "/network/stack/childrenList"
    #         self._api._config_url[device.name] = new_url
    #         #self._delete_ethernet(device, new_url)
    #     for device in self._devices_config:
    #         self._create_ethernet(device)
    #         #self._create_ipv4()

    # def _create_ethernet(self, device):
    #     """Add any scenarios to the api server that do not already exist
    #     """
    #     flag = 1
    #     for ethernet in device.ethernets:
    #         if flag:
    #             # payload = {"itemType": "L2EthernetPlugin"}
    #             url = self._api._config_url[device.name]
    #             response = self._api._request("GET", url)
    #             self._api._config_url["mac_url"] = (
    #                 url + "/" + str(response[-1]["objectID"])
    #             )
    #             eth_url = url + "/" + str(response[-1]["objectID"]) + "/macRangeList/"
    #             ipp_url = url + "/" + str(response[-1]["objectID"]) + "/childrenList/"
    #             mac_url = eth_url + str(
    #                 self._api._request("GET", eth_url)[-1]["objectID"]
    #             )
    #             ip_url = (
    #                 ipp_url
    #                 + str(self._api._request("GET", ipp_url)[-1]["objectID"])
    #                 + "/rangeList/"
    #             )
    #             ip_url = ip_url + str(self._api._request("GET", ip_url)[-1]["objectID"])

    #             vlan_url = url + "/" + str(response[-1]["objectID"]) + "/vlanRangeList/"
    #             vlan_url = vlan_url + str(
    #                 self._api._request("GET", vlan_url)[-1]["objectID"]
    #             )
    #             payload = {"autoMacGeneration": False}
    #             response = self._api._request("PATCH", ip_url, payload)
    #             payload = self._api._set_payload(ethernet, interfaces._ETHERNET)
    #             response = self._api._request("PATCH", mac_url, payload)
    #             self._api._config_url[ethernet.name] = mac_url
    #             self._create_ipv4(ethernet, ip_url, flag)
    #             self._create_vlan(ethernet, vlan_url, flag)
    #             flag = 0
    #         else:
    #             eth_url = self._api._config_url["mac_url"] + "/macRangeList"
    #             payload = self._api._set_payload(ethernet, interfaces._ETHERNET)
    #             response = self._api._request("POST", eth_url, payload)
    #             eth_url = eth_url + "/" + str(response)
    #             ip_url = self._api._config_url["mac_url"] + "/childrenList/"
    #             ip_url = (
    #                 ip_url
    #                 + str(self._api._request("GET", ip_url, option=1)[-1]["objectID"])
    #                 + "/rangeList/"
    #             )
    #             ip_url = ip_url + str(
    #                 self._api._request("GET", ip_url, option=1)[-1]["objectID"]
    #             )

    #             vlan_url = self._api._config_url["mac_url"] + "/vlanRangeList/"
    #             vlan_url = vlan_url + str(
    #                 self._api._request("GET", vlan_url, option=1)[-1]["objectID"]
    #             )
    #             payload = {"autoMacGeneration": False}
    #             response = self._api._request("PATCH", ip_url, payload)
    #             self._api._config_url[ethernet.name] = eth_url
    #             self._create_ipv4(ethernet, ip_url, flag)
    #             self._create_vlan(ethernet, vlan_url, flag)

    # def _delete_ethernet(self, device, url):
    #     """delete any scenarios to the api server that do not already exist"""
    #     response = self._api._request("GET", url, option=1)
    #     payload = {"objectID": response[0]["objectID"]}
    #     response = self._api._request("DELETE", url, payload)

    # def _create_ipv4(self, ethernet, url, flag):
    #     """
    #     Add any ipv4 to the api server that do not already exist
    #     """
    #     ipv4_addresses = ethernet.get("ipv4_addresses")
    #     if ipv4_addresses is None:
    #         return
    #     for ipv4 in ethernet.ipv4_addresses:
    #         payload = self._api._set_payload(ipv4, interfaces._IP)
    #         if payload:
    #             response = self._api._request("PATCH", url, payload)
    #             self._api._config_url[ipv4.name] = url

    # def _create_vlan(self, ethernet, vlan_url, flag):
    #     """
    #     Add any ipv4 to the api server that do not already exist
    #     """

    #     vlans = ethernet.get("vlans")
    #     if vlans is None:
    #         return
    #     for vlan in ethernet.vlans:
    #         payload = {"enabled": True}
    #         response = self._api._request("PATCH", vlan_url, payload)
    #         payload = self._api._set_payload(vlan, interfaces._VLAN)
    #         if payload:
    #             response = self._api._request("PATCH", vlan_url, payload)
    #             self._api._config_url[vlan.name] = vlan_url
