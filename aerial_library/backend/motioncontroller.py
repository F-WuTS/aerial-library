from math import cos, sin, radians
from time import sleep
from typing import Final, Optional, ContextManager, TYPE_CHECKING

from aerial_library.api.errors import FlowDeckNotFound, AlreadyFlying, AlreadyLanded
from aerial_library.backend.position import Position
from aerial_library.backend.util import build_log_config

if TYPE_CHECKING:
    from aerial_library.backend.drone import Drone


_PARAM_X_NAME: Final = "stateEstimate.x"
_PARAM_Y_NAME: Final = "stateEstimate.y"
_PARAM_Z_NAME: Final = "stateEstimate.z"
_PARAM_YAW_NAME: Final = "stateEstimate.yaw"

_SLOW_M_PER_S: Final = 0.25
_SLOW_DEG_PER_S: Final = 45.0

_FAST_M_PER_S: Final = 1.0
_FAST_DEG_PER_S: Final = 180.0

_TAKEOFF_M_PER_S: Final = 0.5
_LANDING_M_PER_S: Final = 0.5

_DISTANCE_THRESHOLD_M: Final = 0.075
_DISTANCE_THRESHOLD_DEG: Final = 2.5

_LANDING_FALL_DISTANCE_M: Final = 0.04
_LANDING_FALL_COOLDOWN_S: Final = 1.0


class MotionController(ContextManager):
    def __init__(self, drone: "Drone", use_fast_mode: bool):
        self._drone = drone

        self._m_per_s = _FAST_M_PER_S if use_fast_mode else _SLOW_M_PER_S
        self._deg_per_s = _FAST_DEG_PER_S if use_fast_mode else _SLOW_DEG_PER_S

        self._is_flying = False
        self._home: Optional[Position] = None
        self._current_pos: Optional[Position] = None
        self._target: Optional[Position] = None

    def __enter__(self):
        if not self._drone.has_deck("bcFlow2"):
            raise FlowDeckNotFound()

        self._register_position_listener()
        self._await_initial_position()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.is_flying:
            self.land()

    @property
    def is_flying(self) -> bool:
        return self._is_flying

    def takeoff(self, height_m: float) -> None:
        if self.is_flying:
            raise AlreadyFlying()

        self._is_flying = True

        self._target.z += height_m
        duration = self._get_flight_duration(
            distance_m=height_m,
            override_m_per_s=_TAKEOFF_M_PER_S,
        )

        self._drone.cf.high_level_commander.takeoff(
            absolute_height_m=self._current_pos.z + height_m,
            yaw=None,  # Leave current yaw unchanged
            duration_s=duration,
        )
        sleep(duration)

        # Correct sideways motion caused by ground effect
        self.change_relative_position()

    def land(self) -> None:
        if not self.is_flying:
            raise AlreadyLanded()

        self._is_flying = False

        self._target.z = self._home.z
        duration = self._get_flight_duration(
            distance_m=self._current_pos.z - self._home.z,
            override_m_per_s=_LANDING_M_PER_S,
        )

        self._drone.cf.high_level_commander.land(
            absolute_height_m=self._home.z + _LANDING_FALL_DISTANCE_M,
            yaw=None,  # Leave current yaw unchanged
            duration_s=duration,
        )
        sleep(duration + _LANDING_FALL_COOLDOWN_S)

    def change_relative_position(
        self,
        forward_m: float = 0,
        left_m: float = 0,
        up_m: float = 0,
        yaw_deg: float = 0,
    ):
        if not self.is_flying:
            raise RuntimeError("Cannot change position, drone is landed")

        psi = radians(self._target.yaw)
        self._target.x += forward_m * cos(psi) - left_m * sin(psi)
        self._target.y += forward_m * sin(psi) + left_m * cos(psi)
        self._target.z += up_m
        self._target.yaw += yaw_deg

        distance_m = self._current_pos.distance_to(self._target)
        distance_deg = self._current_pos.angle_to(self._target)
        duration = self._get_flight_duration(distance_m, distance_deg)

        self._drone.cf.high_level_commander.go_to(
            x=self._target.x,
            y=self._target.y,
            z=self._target.z,
            yaw=radians(self._target.yaw),
            duration_s=duration,
        )

        sleep(duration)

        while (
            self._current_pos.distance_to(self._target) > _DISTANCE_THRESHOLD_M
            or self._current_pos.angle_to(self._target) > _DISTANCE_THRESHOLD_DEG
        ):
            # Wait until the drone settled
            sleep(0.01)

    def _get_flight_duration(
        self,
        distance_m: float = 0,
        distance_deg: float = 0,
        override_m_per_s: float = None,
        override_deg_per_s: float = None,
    ) -> float:
        m_per_s = override_m_per_s or self._m_per_s
        deg_per_s = override_deg_per_s or self._deg_per_s

        time_for_distance = abs(distance_m) / m_per_s
        time_for_angle = abs(distance_deg) / deg_per_s
        return max(time_for_distance, time_for_angle)

    def _register_position_listener(self) -> None:
        self._log_config = build_log_config(
            name=MotionController.__qualname__,
            period_ms=10,
            entry_names={_PARAM_X_NAME, _PARAM_Y_NAME, _PARAM_Z_NAME, _PARAM_YAW_NAME},
        )

        self._drone.cf.log.add_config(self._log_config)
        self._log_config.data_received_cb.add_callback(self._on_data_received)
        self._log_config.start()

    def _await_initial_position(self):
        while self._current_pos is None:
            sleep(0.01)

        pos = self._current_pos
        self._home = pos.copy()
        self._target = pos.copy()

    def _on_data_received(self, timestamp, data, logconfig):
        if data is None:
            return

        try:
            x = data[_PARAM_X_NAME]
            y = data[_PARAM_Y_NAME]
            z = data[_PARAM_Z_NAME]
            yaw = data[_PARAM_YAW_NAME]
        except KeyError:
            return

        self._current_pos = Position(x, y, z, yaw)
