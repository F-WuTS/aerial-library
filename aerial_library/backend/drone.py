from logging import getLogger
from typing import Final, ContextManager

from appdirs import user_cache_dir
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from aerial_library.api.errors import AlreadyConnected, NotConnected
from aerial_library.api.feature import Feature, FlowDeck
from aerial_library.backend.batterystate import BatteryState
from aerial_library.backend.connectionstate import ConnectionState
from aerial_library.backend.motioncontroller import MotionController
from aerial_library.backend.multirangerdeck import MultiRangerDeck
from aerial_library.backend.util import build_log_config

_PARAM_TIMEOUT_S: Final = 5.0
_PARAM_SUPERVISOR_INFO_NAME: Final = "supervisor.info"
_PARAM_BATTERY_LEVEL_NAME: Final = "pm.batteryLevel"
_PARAM_BATTERY_STATE_NAME: Final = "pm.state"


class Drone(ContextManager):
    _log = getLogger(__name__)

    def __init__(self, uri: str, expected_features: set[Feature]):
        self._state = ConnectionState.Disconnected
        self._supervisor_bitmap = 0x0000
        self._battery_level = 0
        self._battery_state = BatteryState.Shutdown

        self._cf_log_handle: LogConfig

        self._scf = SyncCrazyflie(
            link_uri=uri,
            cf=Crazyflie(rw_cache=user_cache_dir(__package__)),
        )

        self.motion_controller = (
            MotionController(self) if FlowDeck in expected_features else None
        )
        self.multi_ranger = (
            MultiRangerDeck(self) if MultiRangerDeck in expected_features else None
        )

    def __enter__(self):
        self._log.info("Entering")

        if self._state != ConnectionState.Disconnected:
            raise AlreadyConnected()

        self._scf.open_link()
        self._state = ConnectionState.Connecting

        self._register_log_listener()

        if self.motion_controller:
            self.motion_controller.__enter__()

        if self.multi_ranger:
            self.multi_ranger.__enter__()

        self._state = ConnectionState.Connected

    def __exit__(self, exc_type, exc_value, traceback):
        self._log.info("Exiting")

        if self._state != ConnectionState.Connected:
            raise NotConnected()

        self._state = ConnectionState.Disconnecting

        if self.motion_controller is not None:
            self.motion_controller.__exit__(exc_value, exc_value, traceback)

        if self.multi_ranger is not None:
            self.multi_ranger.__exit__(exc_value, exc_value, traceback)

        self._cf_log_handle.stop()

        self._state = ConnectionState.Disconnected
        self._scf.close_link()

    def has_deck(self, name: str) -> bool:
        value_str = self.cf.param.get_value(f"deck.{name}", _PARAM_TIMEOUT_S)
        has_deck = bool(int(value_str))
        return has_deck

    @property
    def battery_state(self) -> BatteryState:
        return self._battery_state

    @property
    def battery_level(self) -> int:
        return self._battery_level

    @property
    def can_be_armed(self) -> bool:
        return self._is_supervisor_bit_set(0)

    @property
    def is_armed(self) -> bool:
        return self._is_supervisor_bit_set(1)

    @property
    def auto_arm(self) -> bool:
        return self._is_supervisor_bit_set(2)

    @property
    def can_fly(self) -> bool:
        return self._is_supervisor_bit_set(3)

    @property
    def is_flying(self) -> bool:
        return self._is_supervisor_bit_set(4)

    @property
    def is_tumbled(self) -> bool:
        return self._is_supervisor_bit_set(5)

    @property
    def is_locked(self) -> bool:
        return self._is_supervisor_bit_set(6)

    @property
    def is_crashed(self) -> bool:
        return self._is_supervisor_bit_set(7)

    @property
    def is_high_level_control_active(self) -> bool:
        return self._is_supervisor_bit_set(8)

    @property
    def is_high_level_trajectory_finished(self) -> bool:
        return self._is_supervisor_bit_set(9)

    @property
    def is_high_level_control_disabled(self) -> bool:
        return self._is_supervisor_bit_set(10)

    @property
    def cf(self):
        return self.scf.cf

    @property
    def scf(self) -> SyncCrazyflie:
        if self._state == ConnectionState.Disconnected:
            raise NotConnected()

        return self._scf

    def _register_log_listener(self):
        self._cf_log_handle = build_log_config(
            name=Drone.__qualname__,
            period_ms=20,
            entry_names={
                _PARAM_SUPERVISOR_INFO_NAME,
                _PARAM_BATTERY_LEVEL_NAME,
                _PARAM_BATTERY_STATE_NAME,
            },
        )

        self.cf.log.add_config(self._cf_log_handle)
        self._cf_log_handle.data_received_cb.add_callback(self._on_data_received)
        self._cf_log_handle.start()

    def _on_data_received(self, timestamp, data, logconfig):
        if data is None:
            return

        try:
            supervisor_info = data[_PARAM_SUPERVISOR_INFO_NAME]
            pm_level = data[_PARAM_BATTERY_LEVEL_NAME]
            pm_state = data[_PARAM_BATTERY_STATE_NAME]
        except KeyError:
            return

        self._supervisor_bitmap = supervisor_info
        self._battery_level = pm_level
        self._battery_state = BatteryState(pm_state)

    def _is_supervisor_bit_set(self, bit: int) -> bool:
        return bool(self._supervisor_bitmap & (1 << bit))
