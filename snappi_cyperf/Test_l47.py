import sys

# sys.path.append("C:\\Users\\waseebai\\Documents\\GitHub\\snappi\\artifacts\\snappi")
sys.path.insert(0, "/home/dipendu/otg/open_traffic_generator/snappi/artifacts/snappi")

import snappi

api = snappi.api(location="http://127.0.0.1:5000", verify=False)
config = api.config()

# port_1_ip = config.ports.port(name="p1", location="10.39.44.120")[-1]
# port_2_ip = config.ports.port(name="p2", location="10.39.44.195")[-1]

tx = config.ports.port(name="tx", location="10.39.44.147")[-1]
rx = config.ports.port(name="rx", location="10.39.44.190")[-1]
# port_1_tag = config.ports.port(name="p1", location="user:port1")[-1]
# port_2_tag = config.ports.port(name="p2", location="user:port2")[-1]

(d1, d2) = config.devices.device(name="d1").device(name="d2")
(e1,) = d1.ethernets.ethernet(name="d1.e1")
e1.connection.port_name = "tx"
e1.mac = "01:02:03:04:05:06"
e1.step = "00:00:00:00:00:01"
e1.count = 1
# e1.max_count = 100
e1.mtu = 1488

(e2,) = d2.ethernets.ethernet(name="d2.e2")
e2.connection.port_name = "rx"
e2.mac = "01:02:03:04:06:06"
e2.step = "00:00:00:00:00:01"
e2.count = 2
# e2.max_count = 100
e2.mtu = 1488

(vlan1,) = e1.vlans.vlan(name="vlan1")
vlan1.id = 1
vlan1.priority = 1
vlan1.tpid = "x8100"
vlan1.count = 1
vlan1.step = 1
vlan1.per_count = 1

(vlan2,) = e2.vlans.vlan(name="vlan2")
vlan2.id = 1
vlan2.priority = 1
vlan2.tpid = "x8100"
vlan2.count = 1
vlan2.step = 1
vlan2.per_count = 1

(ip1,) = e1.ipv4_addresses.ipv4(name="e1.ipv4")
ip1.address = "10.0.0.10"
ip1.gateway = "10.0.0.1"
ip1.step = "0.0.0.1"
ip1.count = 1
# ip1.max_count = 1
ip1.prefix = 16

(ip2,) = e2.ipv4_addresses.ipv4(name="e2.ipv4")
ip2.address = "10.0.0.20"
ip2.gateway = "10.0.0.1"
ip2.step = "0.0.0.1"
ip2.count = 1
# ip2.max_count = 1
ip2.prefix = 16

# TCP/UDP configs

(t1,) = d1.tcps.tcp(name="Tcp1")
t1.ip_interface_name = ip1.name
t1.receive_buffer_size = 1111
t1.transmit_buffer_size = 1112
t1.retransmission_minimum_timeout = 100
t1.retransmission_maximum_timeout = 1001
t1.minimum_source_port = 100
t1.maximum_source_port = 101
# t1.data_content_source = "SyntheticData"
# t1.data_content_value = "30000"
# t1.direction = "client_to_server"

(t2,) = d2.tcps.tcp(name="Tcp2")
t2.ip_interface_name = ip2.name
t2.receive_buffer_size = 2222
t2.transmit_buffer_size = 2221
t2.retransmission_minimum_timeout = 200
t2.retransmission_maximum_timeout = 2002
t2.minimum_source_port = 200
t2.maximum_source_port = 202

(http_1,) = d1.https.http(name="HTTP1")
http_1.profile = "Chrome"
http_1.version = "HTTP11"
http_1.connection_persistence = "ConnectionPersistenceStandard"
(http_client,) = http_1.clients.client()
http_client.cookie_reject_probability = False
http_client.max_persistent_requests = 1

(http_2,) = d2.https.http(name="HTTP2")
http_2.profile = "Apache"
http_2.version = "HTTP11"
http_2.connection_persistence = "ConnectionPersistenceEnabled"
(http_server,) = http_2.servers.server()

# (get_a, post_a) = http_client.methods.method().method()
# (get1,) = get_a.get.get()

# get1.destination = "Traffic2_HTTPServer1:80"
# get1.page = "./1b.html"
# get1.destination = "Traffic2_HTTPServer1:80" #real http server ip or emulated http object  get1.destination = "http2:80"\
# get1.name_value_args = "name1=val1"
# for http server emulation
# get1.destination = http_2.name
# (post1,) = post1_a.post.post()
# post1.destination = "Traffic2_HTTPServer1:80"
# post1.page = "./1b.html"
# (delete1,) = delete_a.delete.delete()
# delete1.destination = "Traffic2_HTTPServer1:80"
# delete1.page = "./1b.html"

(tp1,) = config.trafficprofile.trafficprofile()
(segment1, segment2) = tp1.segment.segment().segment()
segment1.name = "Linear segment1"
segment1.duration = 40
# segment1.enable_ramp_up = True
# segment1.ramp_down_time = 50
# segment1.ramp_down_value = 100
# segment1.enable_ramp_down = True
# segment1.ramp_up_time = 60
# segment1.ramp_up_value = 100
segment2.name = "Linear segment2"
segment2.duration = 70
tp1.timeline = [segment1.name, segment2.name]
tp1.objective_type = ["Connections per second", "Simulated users"]
tp1.objective_value = [100, 200]
(obj1, obj2) = tp1.objectives.objective().objective()

print("In test before set_config")
response = api.set_config(config)
print("In test after set_config")
print(response)
api.close()

cs = api.control_state()
cs.app.state = "start"  # cs.app.state.START
response1 = api.set_control_state(cs)
print(response1)
# cs.app.state = "stop"  # cs.app.state.START
# api.set_control_state(cs)
