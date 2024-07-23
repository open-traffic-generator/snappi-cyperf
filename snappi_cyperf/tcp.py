import json
import re
import time
from timer import Timer
from common import Common


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
        response = rest.add_application("TCP App")
        client = True
        for device in self._devices_config:
            #
            self._update_tcp_config(device, client, rest)
            client = False

    def _update_tcp_config(self, device, client, rest):
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
            else:
                rest.set_server_tcp_profile(payload)
