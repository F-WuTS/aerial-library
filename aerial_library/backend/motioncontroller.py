from logging import getLogger
from math import cos, sin, radians
from time import sleep
from typing import Final, Optional, ContextManager, TYPE_CHECKING

from aerial_library.api.errors import (
    AlreadyFlying,
    AlreadyLanded,
    CannotMoveOnGround,
    RequiredDeckNotFound,
)
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
_TAKEOFF_HEIGHT_M: Final = 0.5

_LANDING_M_PER_S: Final = 0.5
_LANDING_FALL_DISTANCE_M: Final = 0.04

_DISTANCE_THRESHOLD_M: Final = 0.075
_DISTANCE_THRESHOLD_DEG: Final = 2.5


class MotionController(ContextManager):
    _log = getLogger(__name__)

    def __init__(self, drone: "Drone"):
        self._drone = drone

        self._m_per_s = _SLOW_M_PER_S
        self._deg_per_s = _SLOW_DEG_PER_S

        self._is_flying = False
        self._home: Optional[Position] = None
        self._current_pos: Optional[Position] = None
        self._target: Optional[Position] = None

    def __enter__(self):
        self._log.info("Entering")

        if not self._drone.has_deck("bcFlow2"):
            raise RequiredDeckNotFound("Flow")

        self._register_position_listener()
        self._await_initial_position()

        self._log.info("Ready")

    def __exit__(self, exc_type, exc_value, traceback):
        self._log.info("Exiting")

        if self.is_flying:
            self.land()

        self._log_config.stop()

    @property
    def is_flying(self) -> bool:
        return self._is_flying

    def set_fast_mode(self, is_on: bool) -> None:
        self._log.info(f"Setting fast mode to {is_on}")

        if is_on:
            self._m_per_s = _FAST_M_PER_S
            self._deg_per_s = _FAST_DEG_PER_S
        else:
            self._m_per_s = _SLOW_M_PER_S
            self._deg_per_s = _SLOW_DEG_PER_S

    def takeoff(self, height_m: float) -> None:
        self._log.info(f"Taking off to {height_m}m")

        if self.is_flying:
            raise AlreadyFlying()

        self._is_flying = True

        # Take off to a fixed height
        duration = self._get_flight_duration(
            distance_m=_TAKEOFF_HEIGHT_M,
            override_m_per_s=_TAKEOFF_M_PER_S,
        )
        self._drone.cf.high_level_commander.takeoff(
            absolute_height_m=self._current_pos.z + _TAKEOFF_HEIGHT_M,
            yaw=None,  # Leave current yaw unchanged
            duration_s=duration,
        )
        sleep(duration)

        # Move to the desired height and correct sideways motion caused by ground effect
        self._target.z += height_m
        self._move_to_target()

    def land(self) -> None:
        self._log.info("Landing")

        if not self.is_flying:
            raise AlreadyLanded()

        self._is_flying = False

        self._target.z = self._home.z
        duration = self._get_flight_duration(
            distance_m=self._current_pos.z - self._target.z,
            override_m_per_s=_LANDING_M_PER_S,
        )

        self._drone.cf.high_level_commander.land(
            absolute_height_m=self._target.z + _LANDING_FALL_DISTANCE_M,
            yaw=None,  # Leave current yaw unchanged
            duration_s=duration,
        )
        sleep(duration)

    def change_relative_position(
        self,
        forward_m: float = 0,
        left_m: float = 0,
        up_m: float = 0,
        yaw_deg: float = 0,
    ):
        change = Position(forward_m, left_m, up_m, yaw_deg)
        self._log.info(f"Changing relative position by {change}")

        psi = radians(self._target.yaw)

        self._target.x += change.x * cos(psi) - change.y * sin(psi)
        self._target.y += change.x * sin(psi) + change.y * cos(psi)
        self._target.z += change.z
        self._target.yaw += change.yaw

        self._move_to_target()

    def _move_to_target(self):
        self._log.debug(f"Moving to {self._target}")

        if not self.is_flying:
            raise CannotMoveOnGround()

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

        # Wait until the drone settled
        while (
            self._current_pos.distance_to(self._target) > _DISTANCE_THRESHOLD_M
            or self._current_pos.angle_to(self._target) > _DISTANCE_THRESHOLD_DEG
        ):
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
