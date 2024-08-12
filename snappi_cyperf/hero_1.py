import sys
import pprint
import socket
import struct
import macaddress
import ipaddress
from copy import deepcopy
from munch import DefaultMunch

# utils
socket_inet_ntoa = socket.inet_ntoa
struct_pack = struct.pack


class MAC(macaddress.MAC):
    formats = ("xx:xx:xx:xx:xx:xx",) + macaddress.MAC.formats


maca = MAC  # optimization so the . does not get executed multiple times

dflt_params = {  # CONFIG VALUE             # DEFAULT VALUE
    "SCHEMA_VER": "0.0.4",
    "DC_START": "220.0.1.1",  # '220.0.1.2'
    "DC_STEP": "0.0.1.0",  # '0.0.1.0'
    "LOOPBACK": "221.0.0.1",  # '221.0.0.1'
    "PAL": "221.1.0.0",  # '221.1.0.1'
    "PAR": "221.2.0.0",  # '221.2.0.1'
    "GATEWAY": "222.0.0.1",  # '222.0.0.1'
    "DPUS": 8,  # 1
    "ENI_START": 1,  # 1
    "ENI_COUNT": 2,  # 32
    "ENI_STEP": 1,  # 1
    "ENI_L2R_STEP": 0,  # 1000
    "VNET_PER_ENI": 1,  # 16 TODO: partialy implemented
    "ACL_NSG_COUNT": 5,  # 5 (per direction per ENI)
    "ACL_RULES_NSG": 1000,  # 1000
    "IP_PER_ACL_RULE": 1,  # 100
    "ACL_MAPPED_PER_NSG": 500,  # 500, efective is 250 because denny are skiped
    "MAC_L_START": "00:1A:C5:00:00:01",
    "MAC_R_START": "00:1B:6E:00:00:01",
    "MAC_STEP_ENI": "00:00:00:18:00:00",  # '00:00:00:18:00:00'
    "MAC_STEP_NSG": "00:00:00:02:00:00",
    "MAC_STEP_ACL": "00:00:00:00:01:00",
    "IP_L_START": "1.1.0.1",  # local, eni
    "IP_R_START": "1.4.0.1",  # remote, the world
    "IP_STEP1": "0.0.0.1",
    "IP_STEP_ENI": "0.64.0.0",
    "IP_STEP_NSG": "0.2.0.0",
    "IP_STEP_ACL": "0.0.1.0",
    "IP_STEPE": "0.0.0.2",
    "TOTAL_OUTBOUND_ROUTES": 200,  # ENI_COUNT * 100K
}

params_dict = deepcopy(dflt_params)

cooked_params_dict = {}
for ip in [
    "IP_STEP1",
    "IP_STEP_ENI",
    "IP_STEP_NSG",
    "IP_STEP_ACL",
    "IP_STEPE",
    "IP_L_START",
    "IP_R_START",
    "PAL",
    "PAR",
    "GATEWAY",
]:
    cooked_params_dict[ip] = int(ipaddress.ip_address((params_dict[ip])))
for mac in [
    "MAC_L_START",
    "MAC_R_START",
    "MAC_STEP_ENI",
    "MAC_STEP_NSG",
    "MAC_STEP_ACL",
]:
    cooked_params_dict[mac] = int(maca(params_dict[mac]))


params = DefaultMunch.fromDict(params_dict)
cooked_params = DefaultMunch.fromDict(cooked_params_dict)


p = params
ip_int = cooked_params


###################################################################################


sys.path.insert(0, "/home/dipendu/otg/open_traffic_generator/snappi/artifacts/snappi")
import snappi


ixl_api = snappi.api(location="http://127.0.0.1:5000", verify=False)
# ixl_api = snappi.api(location="http://127.0.0.1:5000", verify=False, ext="ixload")
ixlc = ixl_api.config()

port_1 = ixlc.ports.port(name="p1", location="10.39.44.147")[-1]
port_2 = ixlc.ports.port(name="p2", location="10.39.44.190")[-1]

c_device = ixlc.devices.add(name="client")
s_device = ixlc.devices.add(name="server")

# c_device.port = port_1
# S_device.port = port_2


for eni_index, eni in enumerate(
    range(p.ENI_START, p.ENI_START + p.ENI_COUNT * p.ENI_STEP, p.ENI_STEP)
):  # Per ENI

    # vtep_remote = socket_inet_ntoa(struct_pack('>L', ip_int.PAR + ip_int.IP_STEP1 * eni_index))
    # gateway_ip =  socket_inet_ntoa(struct_pack('>L', ip_int.GATEWAY + ip_int.IP_STEP1 * eni_index))
    remote_ip_a_eni = ip_int.IP_R_START + eni_index * ip_int.IP_STEP_ENI
    remote_mac_a_eni = ip_int.MAC_R_START + eni_index * ip_int.MAC_STEP_ENI
    gateway_mac = str(maca(remote_mac_a_eni))

    # add mapping for ENI itself SAI_OBJECT_TYPE_ENI_ETHER_ADDRESS_MAP_ENTRY

    r_vni_id = eni + p.ENI_L2R_STEP

    c_eth = c_device.ethernets.add()
    c_eth.name = "NETMAC%d" % eni
    c_eth.mac = str(maca(remote_mac_a_eni))

    c_vlan = c_eth.vlans.add()
    c_vlan.name = "NETVLAN%d" % eni
    c_vlan.id = r_vni_id

    c_ip = c_eth.ipv4_addresses.add()
    c_ip.name = "NETIP%d" % eni
    c_ip.address = socket_inet_ntoa(struct_pack(">L", remote_ip_a_eni))
    c_ip.gateway = "0.0.0.0"
    c_ip.prefix = 10

    eni_ip = socket_inet_ntoa(
        struct_pack(">L", ip_int.IP_L_START + eni_index * ip_int.IP_STEP_ENI)
    )
    eni_mac = str(maca(ip_int.MAC_L_START + eni_index * ip_int.MAC_STEP_ENI))

    # import pdb; pdb.set_trace()

    s_eth = s_device.ethernets.add()
    s_eth.name = "ENIMAC%d" % eni
    s_eth.mac = eni_mac

    s_vlan = s_eth.vlans.add()
    s_vlan.name = "ENIVLAN%d" % eni
    s_vlan.id = eni

    s_ip = s_eth.ipv4_addresses.add()
    s_ip.name = "ENIIP%d" % eni
    s_ip.address = eni_ip
    s_ip.gateway = "0.0.0.0"
    s_ip.prefix = 10


# import pdb; pdb.set_trace()
response = ixl_api.set_config(ixlc)
print(response)
