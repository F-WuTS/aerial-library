from math import sqrt, radians, sin, cos
from time import sleep
from typing import Optional, Final

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from aerial_library.util import build_log_config, has_flow_deck


class Position:
    def __init__(self, x: float, y: float, z: float, yaw: float):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw

    def distance_to(self, other: "Position") -> float:
        return sqrt(
            pow(self.x - other.x, 2)
            + pow(self.y - other.y, 2)
            + pow(self.z - other.z, 2)
        )

    def angle_to(self, other: "Position") -> float:
        diff = (self.yaw - other.yaw + 180) % 360 - 180
        return abs(diff)

    def copy(self) -> "Position":
        return Position(self.x, self.y, self.z, self.yaw)

    def __str__(self) -> str:
        return f'(x: {self.x:2.4f}, y: {self.y:2.4f}, z: {self.z:2.4f}, yaw: {self.yaw:2.4f})'


class DroneActions:
    _PARAM_X_NAME: Final = 'stateEstimate.x'
    _PARAM_Y_NAME: Final = 'stateEstimate.y'
    _PARAM_Z_NAME: Final = 'stateEstimate.z'
    _PARAM_YAW_NAME: Final = 'stateEstimate.yaw'

    _MAX_DISTANCE_M: Final = 0.075
    _MAX_DISTANCE_DEG: Final = 2.5

    def __init__(
            self,
            crazyflie: SyncCrazyflie,
            m_per_s: float,
            deg_per_s: float
    ):
        if not crazyflie.is_link_open():
            raise RuntimeError('Crazyflie is not connected')
        if not has_flow_deck(crazyflie.cf):
            raise RuntimeError('Crazyflie is not equipped with flow deck')
        if m_per_s <= 0:
            raise ValueError(f'{m_per_s=}, but must be positive')
        if deg_per_s <= 0:
            raise ValueError(f'{deg_per_s=}, but must be positive')

        self._crazyflie = crazyflie

        self._m_per_s = m_per_s
        self._deg_per_s = deg_per_s
        self._is_flying = False

        self._log_config: Optional[LogConfig] = None
        self._start: Optional[Position] = None
        self._position: Optional[Position] = None
        self._target: Optional[Position] = None

        self._register_position_listener()

    def takeoff(self, height_m: float) -> None:
        if self.is_flying:
            raise RuntimeError('Cannot take off, already flying')

        self._is_flying = True
        self._target.z += height_m
        duration = self._get_flight_duration(
            distance_m=height_m,
            override_m_per_s=0.5
        )

        self._crazyflie.cf.high_level_commander.takeoff(
            absolute_height_m=self._position.z + height_m,
            yaw=None,
            duration_s=duration
        )
        sleep(duration)

        # Correct sideways motion caused by ground effect
        self._change_relative_position()

    def land(self) -> None:
        if not self.is_flying:
            raise RuntimeError('Cannot land, already landed')

        self._is_flying = False
        self._target.z = self._start.z
        duration = self._get_flight_duration(
            distance_m=self._position.z - self._start.z,
            override_m_per_s=0.5
        )

        self._crazyflie.cf.high_level_commander.land(
            absolute_height_m=self._start.z + 0.04,  # drop for the last few cm to avoid ground effect
            yaw=None,
            duration_s=duration
        )
        sleep(duration + 1)

    def forward(self, distance_m: float) -> None:
        self._change_relative_position(forward=+distance_m)

    def back(self, distance_m: float) -> None:
        self._change_relative_position(forward=-distance_m)

    def left(self, distance_m: float) -> None:
        self._change_relative_position(left=+distance_m)

    def right(self, distance_m: float) -> None:
        self._change_relative_position(left=-distance_m)

    def up(self, distance_m: float) -> None:
        self._change_relative_position(up=+distance_m)

    def down(self, distance_m: float) -> None:
        self._change_relative_position(up=-distance_m)

    def turn_left(self, angle_deg: float) -> None:
        self._change_relative_position(yaw=+angle_deg)

    def turn_right(self, angle_deg: float) -> None:
        self._change_relative_position(yaw=-angle_deg)

    @property
    def is_flying(self) -> bool:
        return self._is_flying

    def _change_relative_position(
            self,
            forward: float = 0,
            left: float = 0,
            up: float = 0,
            yaw: float = 0
    ) -> None:
        if not self.is_flying:
            raise RuntimeError('Cannot change position, drone is landed')

        psi = radians(self._target.yaw)

        self._target.x += forward * cos(psi) - left * sin(psi)
        self._target.y += forward * sin(psi) + left * cos(psi)
        self._target.z += up
        self._target.yaw += yaw

        # print(f'{forward=:1.2f} {left=:1.2f} {up=:1.2f} {yaw=:1.2f} from {str(self._position)} to {str(self._target)}')  # TODO remove debug print

        distance_m = self._position.distance_to(self._target)
        distance_deg = self._position.angle_to(self._target)
        duration = self._get_flight_duration(distance_m, distance_deg)

        self._crazyflie.cf.high_level_commander.go_to(
            x=self._target.x,
            y=self._target.y,
            z=self._target.z,
            yaw=radians(self._target.yaw),
            duration_s=duration
        )

        sleep(duration)
        ang = 0
        while ((lin := self._position.distance_to(self._target)) > DroneActions._MAX_DISTANCE_M
               or (ang := self._position.angle_to(self._target)) > DroneActions._MAX_DISTANCE_DEG):
            # print(f'{lin=:1.4f} {ang=:1.4f}')  # TODO remove debug print & assigns
            sleep(0.01)

    def _get_flight_duration(
            self,
            distance_m: float = 0,
            distance_deg: float = 0,
            override_m_per_s: float = None,
            override_deg_per_s: float = None
    ) -> float:
        m_per_s = override_m_per_s or self._m_per_s
        deg_per_s = override_deg_per_s or self._deg_per_s

        time_for_distance = abs(distance_m) / m_per_s
        time_for_angle = abs(distance_deg) / deg_per_s
        return time_for_distance + time_for_angle

    def _register_position_listener(self) -> None:
        self._log_config = build_log_config(
            name=DroneActions.__qualname__,
            period_ms=10,
            entry_names=(
                DroneActions._PARAM_X_NAME,
                DroneActions._PARAM_Y_NAME,
                DroneActions._PARAM_Z_NAME,
                DroneActions._PARAM_YAW_NAME
            )
        )

        self._crazyflie.cf.log.add_config(self._log_config)
        self._log_config.data_received_cb.add_callback(
            lambda timestamp, data, logconfig: self._update_data(data)
        )

        self._log_config.start()
        while self._position is None:
            sleep(0.01)

        self._start = self._position.copy()
        self._target = self._start.copy()

    def _update_data(self, data) -> None:
        if data is None:
            return

        try:
            x = data[self._PARAM_X_NAME]
            y = data[self._PARAM_Y_NAME]
            z = data[self._PARAM_Z_NAME]
            yaw = data[self._PARAM_YAW_NAME]
        except KeyError:
            return

        self._position = Position(x, y, z, yaw)
        # print('DEBUG_LOG', x, y, z, yaw)  # TODO remove debug print
