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

    _ETHERNET = {"mac": "mac", "mtu": "mtu", "step": "incrementBy", "count": "count"}

    _IP = {
        "address": "ipAddress",
        "gateway": "gatewayAddress",
        "prefix": "prefix",
        "name": "name",
        "step": "incrementBy",
        "count": "count",
    }

    _VLAN = {"id": "firstId", "priority": "priority", "tpid": "tpid", "name": "name"}

    def __init__(self, cyperfapi):
        self._api = cyperfapi

    def config(self, rest):
        """T"""
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "Interface Configuration"):
            self._create_devices(rest)

    def _create_devices(self, rest):
        """Add any scenarios to the api server that do not already exist"""
        for device in self._devices_config:
            self._create_ethernet(device, rest)

    def _create_ethernet(self, device, rest):
        """Add any scenarios to the api server that do not already exist"""
        for ethernet in device.ethernets:
            payload = {
                "MacAuto": False,
                "MacStart": ethernet.mac,
                "MacIncr": ethernet.step,
                "OneMacPerIP": False,
                "Count": ethernet.count,
                "maxCountPerAgent": ethernet.max_count,
            }
            rest.set_eth_range(
                payload,
                int(ethernet.name),
            )
            self._create_ipv4(ethernet, rest)

    def _create_ipv4(self, ethernet, rest):
        """
        Add any ipv4 to the api server that do not already exist
        """
        ipv4_addresses = ethernet.get("ipv4_addresses")
        if ipv4_addresses is None:
            return
        for ipv4 in ethernet.ipv4_addresses:
            print("ipv4 - ", ipv4)
            payload = {
                "IpAuto": False,
                "IpStart": ipv4.address,
                "IpIncr": ipv4.step,
                "Count": ipv4.count,
                "maxCountPerAgent": ipv4.max_count,
                "NetMaskAuto": False,
                "NetMask": ipv4.prefix,
                "GwAuto": False,
                "GwStart": ipv4.gateway,
                "networkTags": ["network " + ipv4.name],
                "Mss": ethernet.mtu - 28,
            }
            rest.set_ip_range(
                payload,
                int(ipv4.name),
                ipv4.ip_range_id,
            )
            self._create_vlan(ethernet, rest, int(ethernet.name), ipv4.ip_range_id)

    def _create_vlan(self, ethernet, rest, network_segment, ip_range_id):
        """
        Add any ipv4 to the api server that do not already exist
        """
        vlans = ethernet.get("vlans")
        if vlans is None:
            return
        for vlan in ethernet.vlans:
            print("vlan tpid : ", vlan.tpid)
            payload = {
                "VlanEnabled": True,
                "VlanId": vlan.id,
                "VlanIncr": vlan.step,
                "Count": vlan.count,
                "CountPerAgent": vlan.per_count,
                "TagProtocolId": 33024,
                "Priority": vlan.priority,
            }
            rest.set_ip_range_innervlan_range(
                payload,
                network_segment,
                ip_range_id,
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
