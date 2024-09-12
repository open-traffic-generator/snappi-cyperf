import ipaddress
import json
import re
import time
from snappi_cyperf.timer import Timer


class objectiveandtimeline(object):
    """
    Args
    ----
    - Cyperfapi (Api): instance of the Api class

    """

    _SEGMENT_TYPES = {
        "step_up_segment": "StepUpSegment",
        "steady_segment": "SteadySegment",
        "step_down_segment": "StepDownSegment",
    }

    _SEGMENT_ID = {
        "step_up_segment": 1,
        "steady_segment": 2,
        "step_down_segment": 3,
    }

    _OBJECTIVE_TYPES = {
        "simulated_user": "Simulated users",
        "throughput_bps": "Throughput",
        "throughput_kbps": "Throughput",
        "throughput_mbps": "Throughput",
        "throughput_gbps": "Throughput",
        "connection_per_sec": "Connections per second",
        "concurrent_connections": "Concurrent connections",
    }

    _OBJECTIVE_UNITS = {
        "throughput_bps": "bps",
        "throughput_kbps": "Kbps",
        "throughput_mbps": "Mbps",
        "throughput_gbps": "Gbps ",
    }

    def __init__(self, cyperfapi):
        self._api = cyperfapi

    def config(self, rest):
        """T"""
        self._config = self._api._l47config
        with Timer(self._api, "Traffic Profile"):
            self._create_objectives(rest)

    def _create_objectives(self, rest):
        trafficprofile_config = self._config.trafficprofile
        for tp in trafficprofile_config:
            primary_objective = True
            for (
                objective_type,
                objective_value,
                objectives,
            ) in zip(
                tp.objective_type,
                tp.objective_value,
                tp.objectives,
            ):
                objective_unit = ""
                if "throughput" in objective_type:
                    objective_unit = self._OBJECTIVE_UNITS[objective_type]

                objective_payload = self._get_objective_payload(
                    objective_type,
                    objective_unit,
                    objective_value,
                    primary_objective,
                )

                if primary_objective:
                    rest.set_primary_objective(objective_payload)
                    timeline_payload = []
                    steady_segment_set = False
                    for segment in tp.segment:
                        if segment.name == "steady_segment":
                            steady_segment_set = True
                        segment_payload = self._get_timeline_payload(
                            segment.name,
                            segment,
                            objective_unit,
                            objective_value,
                        )
                        timeline_payload.append(segment_payload)
                    if steady_segment_set != True:
                        segment_payload = self._get_timeline_payload(
                            "steady_segment",
                            segment,
                            objective_unit,
                            objective_value,
                        )
                        timeline_payload.append(segment_payload)

                    id = 1
                    for payload in timeline_payload:
                        rest.set_primary_timeline(payload, payload["id"])
                        id = id + 1

                    primary_objective = False
                else:
                    rest.set_secondary_objective(objective_payload)
                    rest.set_secondary_objective(objective_payload)

    def _get_objective_payload(
        self,
        objective_type,
        objective_unit,
        objective_value,
        primary_objective,
    ):
        payload = {}
        payload["Type"] = self._OBJECTIVE_TYPES[objective_type]
        if not primary_objective:
            payload["Enabled"] = True
            if objective_value != None:
                payload["ObjectiveValue"] = objective_value
            if objective_type != None:
                payload["ObjectiveUnit"] = objective_unit

        return payload

    def _get_timeline_payload(
        self,
        segment_name,
        segment,
        objective_unit,
        objective_value,
    ):
        payload = ""
        if segment_name == "step_up_segment":
            payload = self._get_segment_payload(
                True,
                self._SEGMENT_ID[segment_name],
                self._SEGMENT_TYPES[segment_name],
                segment.duration,
                segment.rate,
                "",
            )
        if segment_name == "steady_segment":
            payload = self._get_segment_payload(
                True,
                self._SEGMENT_ID[segment_name],
                self._SEGMENT_TYPES[segment_name],
                None,
                objective_value,
                objective_unit,
            )
        if segment_name == "step_down_segment":
            payload = self._get_segment_payload(
                True,
                self._SEGMENT_ID[segment_name],
                self._SEGMENT_TYPES[segment_name],
                segment.duration,
                segment.rate,
                "",
            )

        return payload

    def _get_segment_payload(
        self,
        segment_enabled=None,
        segment_id=None,
        segment_type=None,
        segment_duration=None,
        segment_value=None,
        segment_unit=None,
    ):
        payload = {}
        if segment_enabled != None:
            payload["Enabled"] = segment_enabled
        if segment_id != None:
            payload["id"] = str(segment_id)
        if segment_type != None:
            payload["SegmentType"] = segment_type
        if segment_duration != None:
            payload["Duration"] = segment_duration
        if segment_value != None:
            payload["ObjectiveValue"] = segment_value
        if segment_unit != None:
            payload["ObjectiveUnit"] = segment_unit

        return payload
