import json
import re
import time
from snappi_cyperf.timer import Timer


class http_config:
    """ """

    _HTTP_CLIENT = {
        # "enable_tos": "enableTos",
        # "priority_flow_control_class" : "pfcClass",
        # "precedence_tos" : "precedenceTOS",
        # "delay_tos" : "delayTOS",
        # "throughput_tos"  : "throughputTOS",
        # "reliability_tos"  : "reliabilityTOS",
        # "url_stats_count": "urlStatsCount",
        # "disable_priority_flow_control": "disablePfc",
        # "enable_vlan_priority": "enableVlanPriority",
        # "vlan_priority": "vlanPriority",
        # "esm": "esm",
        # "enable_esm": "enableEsm",
        # "time_to_live_value": "ttlValue",
        # "tcp_close_option" : "tcpCloseOption",
        # "enable_integrity_check_support" : "enableIntegrityCheckSupport",
        # "type_of_service": "tos",
        # "high_perf_with_simulated_user": "highPerfWithSU",
        "profile": "Name",
        "version": "HTTPVersion",
        "connection_persistence": "ConnectionPersistence",
    }
    _HTTP_SERVER = {
        # "enable_tos": "enableTos",
        # "priority_flow_control_class" : "pfcClass",
        # "precedence_tos" : "precedenceTOS",
        # "delay_tos" : "delayTOS",
        # "throughput_tos"  : "throughputTOS",
        # "reliability_tos"  : "reliabilityTOS",
        # "url_stats_count": "urlStatsCount",
        # "disable_priority_flow_control": "disablePfc",
        # "enable_vlan_priority": "enableVlanPriority",
        # "vlan_priority": "vlanPriority",
        # "esm": "esm",
        # "enable_esm": "enableEsm",
        # "time_to_live_value": "ttlValue",
        # "tcp_close_option" : "tcpCloseOption",
        # "enable_integrity_check_support" : "enableIntegrityCheckSupport",
        # "type_of_service": "tos",
        # "high_perf_with_simulated_user": "highPerfWithSU",
        "profile": "Name",
        "version": "HTTPVersion",
        "connection_persistence": "ConnectionPersistence",
    }
    _HTTP_CLIENTS = {
        # "browser_emulation_name": "Name",
        # "version": "httpVersion",
        # "cookie_jar_size": "cookieJarSize",
        # "cookie_reject_probability": "cookieRejectProbability",
        # "enable_cookie_support": "enableCookieSupport",
        # "command_timeout": "commandTimeout",
        # "command_timeout_ms": "commandTimeout_ms",
        # "enable_proxy": "enableHttpProxy",
        # "proxy" : "httpProxy",
        # "keep_alive": "keepAlive",
        # "max_sessions": "maxSessions",
        # "max_streams": "maxStreams",
        # "max_pipeline": "maxPipeline",
        "max_persistent_requests": "ConnectionsMaxTransactions",
        # "exact_transactions": "exactTransactions",
        # "follow_http_redirects": "followHttpRedirects",
        # "enable_decompress_support": "enableDecompressSupport",
        # "enable_per_conn_cookie_support": "enablePerConnCookieSupport",
        # "ip_preference" : "ipPreference",
        # "enable_large_header": "enableLargeHeader",
        # "max_header_len": "maxHeaderLen",
        # "per_header_percent_dist": "perHeaderPercentDist",
        # "enable_auth": "enableAuth",
        # "piggy_back_ack": "piggybackAck",
        # "tcp_fast_open": "tcpFastOpen",
        # "content_length_deviation_tolerance": "contentLengthDeviationTolerance",
        # "disable_dns_resolution_cache": "disableDnsResolutionCache",
        # "enable_consecutive_ips_per_session": "enableConsecutiveIpsPerSession",
        # "enable_achieve_cc_first": "enableAchieveCCFirst",
        # "enable_traffic_distribution_for_cc": "enableTrafficDistributionForCC",
        # "browser_emulation_name": "browserEmulationName",
    }
    _HTTP_SERVERS = {
        # "rst_timeout": "rstTimeout",
        # "enable_http2": "enableHTTP2",
        # "port": "httpPort",
        # "request_timeout": "requestTimeout",
        # "maximum_response_delay": "maxResponseDelay",
        # "minimum_response_delay": "minResponseDelay",
        # "dont_expect_upgrade": "dontExpectUpgrade",
        # "enable_per_server_per_url_stat": "enablePerServerPerURLstat",
        # "url_page_size": "urlPageSize",
        # "enable_chunk_encoding": "enableChunkEncoding",
        # # "integrity_check_option" : "integrityCheckOption",
        # "enable_md5_checksum": "enableMD5Checksum",
    }
    _HTTP_GET = {
        # "destination": "destination",
        # "page": "pageObject",
        # "abort" : "abort",
        # "profile": "profile",
        # "name_value_args": "namevalueargs",
        # "enable_direct_server_return": "enableDi",
    }

    _HTTP_DELETE = {
        # "destination": "destination",
        # "page": "pageObject",
        # "abort": "abort",
        # "profile": "profile",
    }

    _HTTP_POST = {
        # "destination": "destination",
        # "page": "pageObject",
        # "abort": "abort",
        # "profile": "profile",
        # "name_value_args": "namevalueargs",
        # "arguments": "arguments",
        # "sending_chunk_size": "sendingChunkSize",
        # "send_md5_chksum_header": "sendMD5ChkSumHeader",
    }
    _HTTP_PUT = {
        # "destination": "destination",
        # "page": "pageObject",
        # "abort": "abort",
        # "profile": "profile",
        # "name_value_args": "namevalueargs",
        # "arguments": "arguments",
        # "sending_chunk_size": "sendingChunkSize",
        # "send_md5_check_sum_header": "sendMD5ChkSumHeader",
    }
    _HTTP_HEADER = {
        # "destination": "destination",
        # "page": "pageObject",
        # "abort": "abort",
        # "profile": "profile",
        # "name_value_args": "namevalueargs",
    }

    _TCP = {"keep_alive_time": "tcp_keepalive_time"}

    def __init__(self, cyperfapi):
        self._api = cyperfapi

    def config(self, rest):
        """ """
        print("config 1")
        self._devices_config = self._api._l47config.devices
        app_id = rest.add_application("HTTP App")
        # response = rest.get_application_actions(app_id)
        # print("HTTP Actions :- ", response)
        # response = rest.get_application_actions_values(app_id, 1)
        # print("HTTP Action Get values :- ", response)
        # response = rest.get_application_actions_values(app_id, 2)
        # print("HTTP Action POST values :- ", response)
        print("config 2")
        with Timer(self._api, "HTTP client Configurations"):
            self._create_client_app(rest)
            self._create_server_app(rest)

    def _create_client_app(self, rest):
        """Add any scenarios to the api server that do not already exist"""
        print("_create_client_app")
        for device in self._devices_config:
            self._create_http_client(device, rest)

    def _create_http_client(self, device, rest):
        """Add any scenarios to the api server that do not already exist"""
        for http_client in device.https:
            payload = self._api._set_payload(http_client, http_config._HTTP_CLIENT)
            print("payload ", payload)
            for http_clients in http_client.clients:
                new_payload = self._api._set_payload(
                    http_clients, http_config._HTTP_CLIENTS
                )
                payload["ExternalResourceURL"] = (
                    "/api/v2/resources/http-profiles/" + payload["Name"]
                )
                payload.update(new_payload)
                print("client payload - ", payload)
                rest.set_client_http_profile(payload)
                name_payload = {}
                name_payload["Name"] = payload["Name"]
                rest.set_client_http_profile(name_payload)
        # for client in app_config.http_client:
        #     ip_object = self._api.common.get_ip_name(client.client.name)
        #     url = self._api._config_url.get(self._api._ip_list.get(client.client.name))
        #     url = self._api.common.get_community_url(url)
        #     protocol_url = url+"activityList/"
        #     options = {}
        #     options.update({'protocolAndType': "HTTP Client"})
        #     response = self._api._request('POST', protocol_url, options)
        #     protocol_url = protocol_url+response
        #     self._api._config_url[client.client.name] = protocol_url
        #     payload = self._api._set_payload(client.client, client_config._HTTP_CLIENT)
        #     response = self._api._request('PATCH', protocol_url+"/agent", payload)
        #     self._update_tcp_client(app_config, client)
        #     self._create_method(app_config, client, protocol_url)
        # return

    def _create_server_app(self, rest):
        """Add any scenarios to the api server that do not already exist"""
        for device in self._devices_config:
            self._create_http_server(device, rest)

    def _create_http_server(self, device, rest):
        """Add any scenarios to the api server that do not already exist"""
        #
        for http_server in device.https:
            payload = self._api._set_payload(http_server, http_config._HTTP_SERVER)
            for http_servers in http_server.servers:
                payload["ExternalResourceURL"] = (
                    "/api/v2/resources/http-profiles/" + payload["Name"]
                )
                print("server payload - ", payload)
                rest.set_server_http_profile(payload)

    def _update_tcp_client(self, app_config, client):
        # ip_object = self._api.common.get_ip_name(client.client.name)
        for tcp in app_config.tcp:
            # url = self._api._config_url.get(ip_object)
            url = self._api._config_url.get(self._api._ip_list.get(client.client.name))
            url = self._api.common.get_community_url(url)
            tcp_child_url = "%snetwork/globalPlugins" % url
            response_list = self._api._request("GET", tcp_child_url)
            for index in range(len(response_list)):
                if response_list[index]["itemType"] == "TCPPlugin":
                    tcp_url = "%s/%s" % (
                        tcp_child_url,
                        response_list[index]["objectID"],
                    )
                    payload = self._api._set_payload(tcp, client_config._TCP)
                    response = self._api._request("PATCH", tcp_url, payload)

    def _create_method(self, http_client, protocol_url):
        for method in http_client.methods:
            for post in method.post:
                payload = self._api._set_payload(post, client_config._HTTP_POST)
                payload.update({"commandType": "POST"})
                command_url = protocol_url + "/agent/actionList"
                response = self._api._request("POST", command_url, payload)
            for get in method.get:
                payload = self._api._set_payload(get, client_config._HTTP_GET)
                payload.update({"commandType": "GET"})
                command_url = protocol_url + "/agent/actionList"
                response = self._api._request("POST", command_url, payload)
            for delete in method.delete:
                payload = self._api._set_payload(delete, client_config._HTTP_DELETE)
                payload.update({"commandType": "DELETE"})
                command_url = protocol_url + "/agent/actionList"
                response = self._api._request("POST", command_url, payload)
            for put in method.put:
                payload = self._api._set_payload(put, client_config._HTTP_PUT)
                payload.update({"commandType": "PUT"})
                command_url = protocol_url + "/agent/actionList"
                response = self._api._request("POST", command_url, payload)
            for header in method.header:
                payload = self._api._set_payload(header, client_config._HTTP_HEADER)
                payload.update({"commandType": "HEAD"})
                command_url = protocol_url + "/agent/actionList"
                response = self._api._request("POST", command_url, payload)


class server_config:
    """ """

    _HTTP_SERVER = {
        "enable_tos": "enableTos",
        # "priority_flow_control_class" : "pfcClass",
        # "precedence_tos" : "precedenceTOS",
        # "delay_tos" : "delayTOS",
        # "throughput_tos"  : "throughputTOS",
        "url_stats_count": "urlStatsCount",
        "disable_priority_flow_control": "disablePfc",
        "enable_vlan_priority": "enableVlanPriority",
        "vlan_priority": "vlanPriority",
        "esm": "esm",
        "enable_esm": "enableEsm",
        "time_to_live_value": "ttlValue",
        # "tcp_close_option" : "tcpCloseOption",
        "type_of_service": "tos",
        "high_perf_with_simulated_user": "highPerfWithSU",
    }

    _HTTP_SERVERS = {
        "profile": "Name",
        "version": "HTTPVersion",
        "connection_persistence": "ConnectionPersistence",
        "rst_timeout": "rstTimeout",
        "enable_http2": "enableHTTP2",
        "port": "httpPort",
        "request_timeout": "requestTimeout",
        "maximum_response_delay": "maxResponseDelay",
        "minimum_response_delay": "minResponseDelay",
        "dont_expect_upgrade": "dontExpectUpgrade",
        "enable_per_server_per_url_stat": "enablePerServerPerURLstat",
        "url_page_size": "urlPageSize",
        "enable_chunk_encoding": "enableChunkEncoding",
        # "integrity_check_option" : "integrityCheckOption",
        "enable_md5_checksum": "enableMD5Checksum",
    }

    _TCP = {"keep_alive_time": "tcp_keepalive_time"}

    def __init__(self, cyperfapi):
        self._api = cyperfapi

    def config(self):
        """ """
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "HTTP server Configurations"):
            self._create_server_app()

    def _create_server_app(self):
        """Add any scenarios to the api server that do not already exist"""
        for device in self._devices_config:
            self._create_http_server(device)

    def _create_http_server(self, device):
        """Add any scenarios to the api server that do not already exist"""
        for http in device.https:
            for http_server in http.servers:
                # ip_object = self._ip_list(server.server.name)
                # ip_object = "e2.ipv4"
                url = self._api._config_url.get(http.tcp_name)
                url = self._api.common.get_community_url(url)
                # url = self._api._cyperf+"cyperf/test/activeTest/communityList/1"
                protocol_url = url + "activityList/"
                options = {}
                options.update({"protocolAndType": "HTTP Server"})
                response = self._api._request("POST", protocol_url, options)
                protocol_url = protocol_url + response
                # self._api._config_url[server.server.name] = protocol_url
                payload = self._api._set_payload(http, server_config._HTTP_SERVER)
                response = self._api._request("PATCH", protocol_url + "/agent", payload)
                payload = self._api._set_payload(
                    http_server, server_config._HTTP_SERVERS
                )
                response = self._api._request("PATCH", protocol_url + "/agent", payload)
            del http
            # self._update_tcp_server(app_config, server)

    def _update_tcp_server(self, app_config, server):
        # ip_object = self._api.common.get_ip_name(self._server_config, server.server.name)
        for tcp in app_config.tcp:
            url = self._api._config_url.get(self._api._ip_list.get(server.server.name))
            # url = self._api._config_url.get(ip_object)
            url = self._api.common.get_community_url(url)
            tcp_child_url = "%snetwork/globalPlugins" % url
            response_list = self._api._request("GET", tcp_child_url)
            for index in range(len(response_list)):
                if response_list[index]["itemType"] == "TCPPlugin":
                    tcp_url = "%s/%s" % (
                        tcp_child_url,
                        response_list[index]["objectID"],
                    )
                    payload = self._api._set_payload(tcp, server_config._TCP)
                    response = self._api._request("PATCH", tcp_url, payload)
