import inspect
import json
import time, re
import sys
import logging

# import ixrestutils as http_transport
from collections import namedtuple

# import sys
# sys.path.insert(0, "/home/dipendu/otg/open_traffic_generator/snappi/artifacts/snappi")
import snappi
from snappi_cyperf.RESTasV3 import RESTasV3
import snappi_cyperf.ixrestutils as http_transport
from snappi_cyperf.ports import port
from snappi_cyperf.interface import interfaces
from snappi_cyperf.tcp import tcp_config
from snappi_cyperf.http_config import http_config
from snappi_cyperf.objectiveandtimeline import objectiveandtimeline

# from snappi_cyperf.http_config import client_config

# from snappi_cyperf.http_server_config import server_config
from snappi_cyperf.logger import setup_cyperf_logger
from snappi_cyperf.common import Common
from snappi_cyperf.exceptions import Snappil47Exception


# from protocols import protocols
# from snappi_cyperf.chassis import chassis
# from stats import stats

WAP_USERNAME = "admin"
WAP_PASSWORD = "CyPerf&Keysight#1"
WAP_CLIENT_ID = "clt-wap"
TOKEN_ENDPOINT = "/auth/realms/keysight/protocol/openid-connect/token"


class Api(snappi.Api):
    """ """

    def __init__(
        self,
        host,
        version,
        username,
        password,
        gateway_port=8080,
        log_level="info",
        **kwargs,
    ):
        """Create a session
        - address (str): The ip address of the TestPlatform to connect to
        where test sessions will be created or connected to.
        - port (str): The rest port of the TestPlatform to connect to.
        - username (str): The username to be used for authentication
        - password (str): The password to be used for authentication
        """
        print("In cyperfAPI init")
        super().__init__(**kwargs)
        #    host='https://127.0.0.1:11009' if host is None else host
        # )
        self.rest = RESTasV3(
            ipAddress=host,
            username=WAP_USERNAME,
            password=WAP_PASSWORD,
            client_id=WAP_CLIENT_ID,
        )
        self._host = host
        self._address, self._port = self._get_addr_port(self._host)
        self._username = username
        self._password = password
        self._config_url = {}
        self._network_segments = {}
        self._ip_ranges = {}
        self.configID = None
        self.session_id = None

        self.cyperf_version = version
        self._gateway_port = gateway_port
        self._l4config = None
        self._assistant = None
        self._config_type = self.config()
        self.interfaces = interfaces(self)
        self.tcp = tcp_config(self)
        self.common = Common()
        self.http = http_config(self)
        self.objectiveandtimeline = objectiveandtimeline(self)
        # self.http_sr = server_config(self)
        self.port = port(self)
        self._log_level = (
            logging.INFO if kwargs.get("loglevel") is None else kwargs.get("loglevel")
        )
        self.logger = setup_cyperf_logger(self.log_level, module_name=__name__)
        # self.protocols = protocols(self)
        # self.chassis = chassis(self)
        # self.stats = stats(self)

    def _get_addr_port(self, host):
        items = host.split("/")
        items = items[-1].split(":")

        addr = items[0]
        if len(items) == 2:
            return addr, items[-1]
        else:
            if host.startswith("https"):
                return addr, "443"
            else:
                return addr, "80"

    @property
    def _config(self):
        return self._config

    @property
    def log_level(self):
        return self._log_level

    def _request_detail(self):
        request_detail = snappi.Warning()
        errors = self._errors
        warnings = list()
        if errors:
            Snappil47Exception(errors)
        warnings.append("")
        request_detail.warnings = warnings
        return request_detail

    def set_config(self, config):
        """Set or update the configuration"""
        try:
            if isinstance(config, (type(self._config_type), str)) is False:
                raise TypeError("The content must be of type Union[Config, str]")

            if isinstance(config, str) is True:
                config = self._config_type.deserialize(config)
            self._config_objects = {}
            self._device_encap = {}
            self._cyperf_objects = {}
            self._connect()
            # self._ip_list = self.common.get_protocol_ip(config)
            self._l47config = config
            self.interfaces.config(self.rest)
            self.tcp.config(self.rest)
            self.http.config(self.rest)
            # self.objectiveandtimeline.config(self.rest)
            self.port.config(self.rest)
            # self._apply_config()
        except Exception as err:
            self.logger.info(f"error:{err}")
            raise Snappil47Exception(err)
        return self._request_detail()

    def add_error(self, error):
        """Add an error to the global errors"""
        if isinstance(error, str) is False:
            self._errors.append("%s %s" % (type(error), str(error)))
        else:
            self._errors.append(error)

    def get_config(self):
        return self._l47config

    def set_control_state(self, config):
        try:
            if config.app.state == "start":
                self.start_test(self.rest)

            elif config.app.state == "stop":
                self.stop_test(self.rest)
            elif config.app.state == "abort":
                self.abort_test(self.rest)
        except Exception as err:
            self.logger.info(f"error:{err}")
            raise Snappil47Exception(err)
        return self._request_detail()

    def stats(self, config):
        """Set or update the configuration"""
        try:
            if isinstance(config, (type(self._config_type), str)) is False:
                raise TypeError("The content must be of type Union[Config, str]")

            if isinstance(config, str) is True:
                config = self._config_type.deserialize(config)
            self._config = config
        except Exception as err:
            print(err)

    def _apply_config(self):
        """
        Apply configs
        """

        url = self._cyperf + "cyperf/test/operations/applyConfiguration"
        payload = {}
        reply = self._request("POST", url, payload, option=1)
        if not reply.ok:
            raise Exception(reply.text)
        self._wait_for_action_to_finish(reply, url)

    def start_test(self, rest):
        """
        start test
        """
        rest.start_test()

    def stop_test(self, rest):
        """
        stop test
        """
        rest.stop_test()

    def abort_test(self, rest):
        """
        abort test
        """
        rest.abort_test()

    def get_current_state(self):
        """
        This method gets the test current state. (for example - running, unconfigured, ..)
        """
        url = "%s/cyperf/test/activeTest" % (self._cyperf)
        reply = self._request("GET", url, option=1)
        return reply["currentState"]

    def strip_api_and_version_from_url(self, url):
        """
        #remove the slash (if any) at the beginning of the url
        """
        if url[0] == "/":
            url = url[1:]
        url_elements = url.split("/")
        if "api" in url:
            # strip the api/v0 part of the url
            url_elements = url_elements[2:]
        return "/".join(url_elements)

    def session_assistance(self):
        """ """
        # self.connection = http_transport.get_connection(
        #     self._host, self._gateway_port, http_redirect=True
        # )
        # session_url = "sessions"
        # data = {"cyperfVersion": self.cyperf_version}
        # data = json.dumps(data)
        # reply = self.connection.http_post(url=session_url, data=data)
        # if not reply.ok:
        #     raise Exception(reply.text)
        # try:
        #     new_obj_path = reply.headers["location"]
        # except:
        #     raise Exception(
        #         "Location header is not present. Please check if the action was created successfully."
        #     )
        # session_id = new_obj_path.split("/")[-1]
        # self._cyperf = "%s/%s" % (session_url, session_id)
        # start_session_url = "%s/operations/start" % (self._cyperf)
        # reply = self.connection.http_post(url=start_session_url, data={})
        # if not reply.ok:
        #     Snappil47Exception.status_code = reply.status_code
        #     raise Exception(reply.text)
        # action_result_url = reply.headers.get("location")
        # if action_result_url:
        #     action_result_url = self.strip_api_and_version_from_url(action_result_url)
        #     action_finished = False
        #     while not action_finished:
        #         action_status_obj = self.connection.http_get(url=action_result_url)
        #         if action_status_obj.state == "finished":
        #             if action_status_obj.status == "Successful":
        #                 action_finished = True
        #                 self._cyperf = self._cyperf + "/"
        #                 self.logger.info(
        #                     "Connected to L47, Session ID:%s" % (self._cyperf)
        #                 )
        #                 msg = "Successfully connected to cyperf"
        #                 # self.add_error(msg)
        #                 self.warning(msg)
        #             else:
        #                 error_msg = (
        #                     "Error while executing action '%s'." % start_session_url
        #                 )
        #                 if action_status_obj.status == "Error":
        #                     error_msg += action_status_obj.error
        #                 raise Exception(error_msg)
        #         else:
        #             time.sleep(0.1)
        # self.configID = "appsec-appmix-and-attack"
        # self.configID = "appsec-empty-config"
        self.configID = "appsec-appmix"
        response = self.rest.create_session(self.configID)
        if response:
            self.session_id = response.json()[0]["id"]
            print("Config successfully opened, session ID: {}".format(self.session_id))

    def _connect(self):
        """Connect to s Cyperf API Server."""
        self._errors = []
        self.logger = setup_cyperf_logger(self.log_level, module_name=__name__)
        self.logger.info("Connecting to Cyperf")
        if self._assistant is None:
            self.session_assistance()

    def _request(
        self, method, url, payload=None, params=None, headers=None, option=None
    ):
        """ """
        data = json.dumps(payload)
        response = self.connection._request(
            method=method,
            url=url,
            data=data,
            params=params,
            headers=headers,
            option=option,
        )
        return response

    def _wait_for_action_to_finish(self, reply_obj, action_url):
        """
        This method waits for an action to finish executing. after a POST request is sent in order to start an action,
        The HTTP reply will contain, in the header, a 'location' field, that contains an URL.
        The action URL contains the status of the action. we perform a GET on that URL every 0.5 seconds until the action finishes with a success.
        If the action fails, we will throw an error and print the action's error message.
        Args:
        - reply_obj the reply object holding the location
        - rt_handle - the url pointing to the operation
        """
        action_result_url = reply_obj.headers.get("location")
        if action_result_url:
            action_result_url = self.strip_api_and_version_from_url(action_result_url)
            action_finished = False
            while not action_finished:
                action_status_obj = self._request("GET", action_result_url)
                # action_status_obj = rt_handle.invoke('http_get', url=action_result_url)
                if action_status_obj.state == "finished":
                    if action_status_obj.status == "Successful":
                        action_finished = True
                    else:
                        error_msg = "Error while executing action '%s'." % action_url
                        if action_status_obj.status == "Error":
                            error_msg += action_status_obj.error
                        raise Exception(error_msg)
                else:
                    time.sleep(0.1)

    def strip_api_and_version_from_url(self, url):
        """
        #remove the slash (if any) at the beginning of the url
        """
        if url[0] == "/":
            url = url[1:]
        url_elements = url.split("/")
        if "api" in url:
            # strip the api/v0 part of the url
            url_elements = url_elements[2:]
        return "/".join(url_elements)

    def _get_url(self, parent, child):
        """ """
        try:
            pattern = re.search(r"(.*)(\{id\})(.*)", child)
            if pattern:
                url1 = parent + pattern.group(1)
                url2 = pattern.group(3)
                return (url1, url2)
        except Exception:
            raise Exception(
                "can not get url for parent %s and child %s" % (parent, child)
            )

    def _set_payload(self, snappi_obj, attr_map):
        properties = snappi_obj._properties
        payload = {}
        for snappi_attr, ixl_map in attr_map.items():
            value = snappi_obj.get(snappi_attr)
            payload[ixl_map] = value

        # for prop_name in properties:

        #     if prop_name != 'url' and isinstance(properties[prop_name], (str, int, float, list)):
        #         prop_name_new = self._convert_camel(prop_name)
        #         payload[prop_name_new] = properties[prop_name]
        return payload

    def _convert_camel(self, argument):
        word_regex_pattern = re.compile("[^A-Za-z]+")
        words = word_regex_pattern.split(argument)
        return "".join(w.lower() if i == 0 else w.title() for i, w in enumerate(words))

    def info(self, message):
        print("working %s" % message)

    def warning(self, message):
        logging.warning(message)
