import sys

# sys.path.append("C:\\Users\\waseebai\\Documents\\GitHub\\snappi\\artifacts\\snappi")
sys.path.insert(0, "/home/dipendu/otg/open_traffic_generator/snappi/artifacts/snappi")

import snappi

api = snappi.api(location="http://127.0.0.1:5000", verify=False)
config = api.config()

# port_1_ip = config.ports.port(name="p1", location="10.39.44.120")[-1]
# port_2_ip = config.ports.port(name="p2", location="10.39.44.195")[-1]

port_1_ip = config.ports.port(name="p1", location="10.39.44.147")[-1]
port_2_ip = config.ports.port(name="p2", location="10.39.44.190")[-1]
# port_1_tag = config.ports.port(name="p1", location="user:port1")[-1]
# port_2_tag = config.ports.port(name="p2", location="user:port2")[-1]

(d1, d2) = config.devices.device(name="d1").device(name="d2")
(e1,) = d1.ethernets.ethernet(name="d1.e1")
e1.connection.port_name = "p1"
e1.mac = "70:9C:91:69:00:00"
e1.step = "00:00:00:00:00:01"
e1.count = 1
e1.max_count = 100
e1.mtu = 1450

(e2,) = d2.ethernets.ethernet(name="d2.e2")
e2.connection.port_name = "p2"
e2.mac = "7C:5D:68:26:00:00"
e2.step = "00:00:00:00:00:02"
e2.count = 2
e2.max_count = 200
e2.mtu = 1450

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
ip1.address = "173.173.173.10"
ip1.gateway = "173.173.173.30"
ip1.step = "0.0.0.1"
ip1.count = 1
ip1.max_count = 1
ip1.prefix = 16
ip1.ip_range_id = 1

(ip2,) = e2.ipv4_addresses.ipv4(name="e2.ipv4")
ip2.address = "173.173.173.30"
ip2.gateway = "173.173.173.10"
ip2.step = "0.0.0.2"
ip2.count = 2
ip2.max_count = 2
ip2.prefix = 12
ip2.ip_range_id = 1

# TCP/UDP configs

(t1,) = d1.tcps.tcp(name="Tcp1")
t1.ip_interface_name = ip1.name
t1.receive_buffer_size = 1111
t1.transmit_buffer_size = 1112
t1.retransmission_minimum_timeout = 100
t1.retransmission_maximum_timeout = 1001
t1.minimum_source_port = 100
t1.maximum_source_port = 101

(t2,) = d2.tcps.tcp(name="Tcp2")
t2.ip_interface_name = ip2.name
t2.receive_buffer_size = 2222
t2.transmit_buffer_size = 2221
t2.retransmission_minimum_timeout = 200
t2.retransmission_maximum_timeout = 2002
t2.minimum_source_port = 200
t2.maximum_source_port = 202

# (http_1,) = d1.https.http(name="HTTP1")
# http_1.tcp_name = t1.name  # UDP configs can be mapped http.transport = udp_1.name
# http_1.enable_tos = False
# http_1.priority_flow_control_class = "v10"
# http_1.precedence_tos = "v20"
# http_1.delay_tos = "v10"
# http_1.throughput_tos = "v10"
# http_1.url_stats_count = 10
# http_1.disable_priority_flow_control = 0
# http_1.enable_vlan_priority = False
# http_1.vlan_priority = 0
# http_1.esm = 1460
# http_1.enable_esm = False
# http_1.time_to_live_value = 64
# http_1.tcp_close_option = "v10"
# http_1.enable_integrity_check_support = False
# http_1.type_of_service = 0
# http_1.high_perf_with_simulated_user = False
# (http_client,) = http_1.clients.client()
# http_client.cookie_jar_size = 100
# http_client.version = "1"
# http_client.cookie_reject_probability = True
# http_client.enable_cookie_support = False
# http_client.command_timeout = 600
# http_client.command_timeout_ms = 0
# http_client.enable_proxy = False
# http_client.keep_alive = False
# http_client.max_sessions = 3
# http_client.max_streams = 1
# http_client.max_pipeline = 1
# http_client.max_persistent_requests = 1
# http_client.exact_transactions = 0
# http_client.follow_http_redirects = False
# http_client.enable_decompress_support = False
# http_client.enable_per_conn_cookie_support = False
# http_client.ip_preference = "v10"
# http_client.enable_large_header = False
# http_client.max_header_len = 1024
# http_client.per_header_percent_dist = False
# http_client.enable_auth = False
# http_client.piggy_back_ack = True
# http_client.tcp_fast_open = False
# http_client.content_length_deviation_tolerance = 0
# http_client.disable_dns_resolution_cache = False
# http_client.enable_consecutive_ips_per_session = False
# http_client.enable_achieve_cc_first = False
# http_client.enable_traffic_distribution_for_cc = False
# http_client.browser_emulation_name = "Browser1"

# http_1.client(endpoints_allow_inbound)

# get1 = http1.client.methods.add("get")
# get1.page = "./1b.html"
# get1.destination = "10.0.10.1" #real http server ip or emulated http object  get1.destination = "http2:80"
# for http server emulation
# get1.destination = http_2.name
# (http_2,) = d2.https.http(name="HTTP2")
# http_2.tcp_name = t2.name  # UDP configs can be mapped http.transport = udp_2.name
# http_2.enable_tos = False
# http_2.priority_flow_control_class = "v10"
# http_2.precedence_tos = "v20"
# http_2.delay_tos = "v10"
# http_2.throughput_tos = "v10"
# http_2.url_stats_count = 10
# http_2.disable_priority_flow_control = 0
# http_2.enable_vlan_priority = False
# http_2.vlan_priority = 0
# http_2.esm = 1460
# http_2.enable_esm = False
# http_2.time_to_live_value = 64
# http_2.tcp_close_option = "v10"
# http_2.enable_integrity_check_support = False
# http_2.type_of_service = 0
# http_2.high_perf_with_simulated_user = (
#     False  # UDP configs can be mapped http.transport = udp_2.name
# )
# # http_2.server(endpoints_allow_outbound)
# (http_server,) = http_2.servers.server()
# http_server.rst_timeout = 100
# http_server.enable_http2 = False
# http_server.port = 80
# http_server.request_timeout = 300
# http_server.maximum_response_delay = 0
# http_server.minimum_response_delay = 0
# http_server.dont_expect_upgrade = False
# http_server.enable_per_server_per_url_stat = False
# http_server.url_page_size = 1024
# http_server.enable_chunk_encoding = False
# http_server.enable_md5_checksum = False

# (get_a, delete_a) = http_client.methods.method().method()
# (get1,) = get_a.get.get()
# get1.destination = "Traffic2_HTTPServer1:80"
# get1.page = "./1b.html"
# get1.destination = "Traffic2_HTTPServer1:80" #real http server ip or emulated http object  get1.destination = "http2:80"
# for http server emulation
# get1.destination = http_2.name
# (post1,) = post1_a.post.post()
# post1.destination = "Traffic2_HTTPServer1:80"
# post1.page = "./1b.html"
# (delete1,) = delete_a.delete.delete()
# delete1.destination = "Traffic2_HTTPServer1:80"
# delete1.page = "./1b.html"

# (tp1,) = config.trafficprofile.trafficprofile()
# # traffic_profile = config.TrafficProfiles.TrafficProfile(name = "traffic_profile_1")
# tp1.app = [
#     http_1.name,
#     http_2.name,
# ]  # traffic_profile_cps.app - "app" using it for reference can be some generic name for traffic profile on which traffic has to flow

# tp1.objective_type = ["CPS", "simulation_user"]
# tp1.objective_value = [100, 100]
# (segment1, segment2) = tp1.segment.segment().segment()
# segment1.name = "Linear segment1"
# segment1.start = 0
# segment1.duration = 10
# segment1.rate = 10
# segment1.target = 100
# segment2.name = "Linear segment2"
# segment2.start = 0
# segment2.duration = 10
# segment2.rate = 10
# segment2.target = 100
# tp1.timeline = [segment1.name, segment2.name]
# obj1 = tp1.objectives.concurrent_connections
# obj1.ramp_down_time = 100

print("In test before set_config")
response = api.set_config(config)
print("In test after set_config")
print(response)
api.close()

# cs = api.control_state()
# cs.app.state = "start"  # cs.app.state.START
# response1 = api.set_control_state(cs)
# print(response1)
# cs.app.state = "stop"  # cs.app.state.START
# api.set_control_state(cs)
