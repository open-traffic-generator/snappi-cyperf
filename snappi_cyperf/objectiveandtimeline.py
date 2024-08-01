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
                segment,
                timeline,
                objective_type,
                objective_value,
                objectives,
            ) in zip(
                tp.segment,
                tp.timeline,
                tp.objective_type,
                tp.objective_value,
                tp.objectives,
            ):
                objective_payload = self._get_objective_payload(
                    objective_type, objective_value, objectives, primary_objective
                )

                if primary_objective:
                    rest.set_primary_objective(objective_payload)
                    timeline_payload = self._get_timeline_payload(
                        segment,
                        objective_value,
                        objectives,
                    )
                    id = 1
                    for payload in timeline_payload:
                        rest.set_primary_timeline(payload, id)
                        id = id + 1
                    primary_objective = False
                else:
                    rest.set_secondary_objective(objective_payload)
                    rest.set_secondary_objective(objective_payload)

    def _get_objective_payload(
        self, objective_type, objective_value, objectives, primary_objective
    ):
        payload = {}
        payload["Type"] = objective_type
        if objectives.simulated_user.max_pending_user != None:
            payload["MaxPendingSimulatedUsers"] = (
                objectives.simulated_user.max_pending_user
            )
        if objectives.simulated_user.max_user_per_second != None:
            payload["MaxSimulatedUsersPerInterval"] = (
                objectives.simulated_user.max_user_per_second
            )
        if not primary_objective:
            payload["Enabled"] = True
            if objective_value != None:
                payload["ObjectiveValue"] = objective_value
            if objectives.throughput.throughput_unit != None:
                payload["ObjectiveUnit"] = objectives.throughput.throughput_unit

        return payload

    def _get_timeline_payload(
        self,
        segment,
        objective_value,
        objectives,
    ):
        step_up_payload = self._get_segment_payload(
            segment.enable_ramp_up,
            "1",
            "StepUpSegment",
            segment.ramp_up_time,
            segment.ramp_up_value,
            "",
        )
        step_steady_payload = self._get_segment_payload(
            True,
            "2",
            "SteadySegment",
            segment.duration,
            objective_value,
            objectives.throughput.throughput_unit,
        )
        step_down_payload = self._get_segment_payload(
            segment.enable_ramp_down,
            "3",
            "StepDownSegment",
            segment.ramp_down_time,
            segment.ramp_down_value,
            "",
        )

        payload = [step_up_payload, step_steady_payload, step_down_payload]

        return payload

    def _get_segment_payload(
        self,
        segment_enabled,
        segment_id,
        segment_type,
        segment_duration,
        segment_value,
        segment_unit,
    ):
        payload = {}
        payload["Enabled"] = segment_enabled
        payload["id"] = segment_id
        payload["SegmentType"] = segment_type
        payload["Duration"] = segment_duration
        if segment_value != None:
            payload["ObjectiveValue"] = segment_value
        if segment_unit != None:
            payload["ObjectiveUnit"] = segment_unit

        return payload
