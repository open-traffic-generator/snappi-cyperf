import json
import re
import time
from snappi_cyperf.timer import Timer
from snappi_cyperf.common import Common


class tcp_config(Common):
    """Transforms OpenAPI objects into IxNetwork objects
    - Lag to /lag
    Args
    ----
    - Cyperfapi (Api): instance of the Api class

    """

    _TCP = {
        "receive_buffer_size": "RxBuffer",
        "transmit_buffer_size": "TxBuffer",
        "retransmission_minimum_timeout": "MinRto",
        "retransmission_maximum_timeout": "MaxRto",
        "minimum_source_port": "MinSrcPort",
        "maximum_source_port": "MaxSrcPort",
    }

    def __init__(self, cyperfapi):
        self._api = cyperfapi

    def config(self, rest):
        """ """
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "Tcp Configurations"):
            self._update_tcp(rest)

    def _update_tcp(self, rest):
        """Add any scenarios to the api server that do not already exist"""
        app_id = rest.add_application("TCP App")
        response = rest.get_application_actions(app_id)
        action_id = response[-1]["id"]
        client = True
        for device in self._devices_config:
            #
            self._update_tcp_config(device, client, rest, app_id, action_id)
            client = False

    def _update_tcp_config(self, device, client, rest, app_id, action_id):
        """Add any scenarios to the api server that do not already exist"""
        for tcp in device.tcps:
            payload = self._api._set_payload(tcp, tcp_config._TCP)
            payload["DeferAccept"] = True
            payload["PingPong"] = True
            payload["CloseWithReset"] = False
            payload["EcnEnabled"] = False
            payload["TimestampHdrEnabled"] = True
            payload["RecycleTwEnabled"] = True
            payload["ReuseTwEnabled"] = True
            payload["SackEnabled"] = False
            payload["WscaleEnabled"] = False
            payload["PmtuDiscDisabled"] = False
            payload["Reordering"] = False
            if client:
                rest.set_client_tcp_profile(payload)
                # self._update_tcp_properties(tcp, rest, app_id, action_id)
            else:
                rest.set_server_tcp_profile(payload)

    # def _update_tcp_properties(self, tcp, rest, app_id, action_id):
    #     payload_data_content = {}
    #     payload_data_content["Source"] = tcp.data_content_source
    #     payload_data_content["Value"] = tcp.data_content_value
    #     rest.set_application_actions_values(payload_data_content, app_id, action_id, 0)
    #     payload_direction = {}
    #     payload_direction["Value"] = tcp.direction
    #     rest.set_application_actions_values(payload_direction, app_id, action_id, 1)
