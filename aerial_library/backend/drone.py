from logging import getLogger
from typing import Optional, Final, ContextManager

from appdirs import user_cache_dir
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

from aerial_library.api.errors import AlreadyConnected, AlreadyDisconnected
from aerial_library.api.feature import Feature
from aerial_library.backend.batterystate import BatteryState
from aerial_library.backend.connectionstate import ConnectionState
from aerial_library.backend.motioncontroller import MotionController
from aerial_library.backend.multirangerdeck import MultiRangerDeck
from aerial_library.backend.util import build_log_config


_PARAM_TIMEOUT_S: Final = 5.0


class Drone(ContextManager):
    _log = getLogger(__name__)

    def __init__(self, uri: str, expected_features: set[Feature]):
        cache_dir = user_cache_dir(__package__)

        self._scf = SyncCrazyflie(link_uri=uri, cf=Crazyflie(rw_cache=cache_dir))
        self._state = ConnectionState.Disconnected

        self.motion_controller = self._load_motion_controller(expected_features)
        self.multi_ranger = self._load_multi_ranger(expected_features)

    @property
    def cf(self):
        return self.scf.cf

    @property
    def scf(self) -> SyncCrazyflie:
        if self._state == ConnectionState.Disconnected:
            raise RuntimeError("Crazyflie is not connected")

        return self._scf

    def __enter__(self):
        self._log.info("Entering")

        if self._state != ConnectionState.Disconnected:
            raise AlreadyConnected()

        self._scf.open_link()
        self._state = ConnectionState.Connecting

        if self.motion_controller:
            self.motion_controller.__enter__()

        if self.multi_ranger:
            self.multi_ranger.__enter__()

        self._state = ConnectionState.Connected

    def __exit__(self, exc_type, exc_value, traceback):
        self._log.info("Exiting")

        if self._state != ConnectionState.Connected:
            raise AlreadyDisconnected()

        self._state = ConnectionState.Disconnecting

        if self.motion_controller is not None:
            self.motion_controller.__exit__(exc_value, exc_value, traceback)

        if self.multi_ranger is not None:
            self.multi_ranger.__exit__(exc_value, exc_value, traceback)

        self._state = ConnectionState.Disconnected
        self._scf.close_link()

    def get_battery_information(self) -> tuple[BatteryState, int]:
        log_config = build_log_config(
            "Battery Information",
            1000,
            {"pm.batteryLevel", "pm.state"},
        )

        with SyncLogger(self.cf, log_config) as log:
            data = log.next()[1]

            level = data["pm.batteryLevel"]
            state = data["pm.state"]

            return BatteryState(state), level

    def has_deck(self, name: str) -> bool:
        value_str = self.cf.param.get_value(f"deck.{name}", _PARAM_TIMEOUT_S)
        has_deck = bool(int(value_str))
        return has_deck

    def _load_motion_controller(
        self,
        features: set[Feature],
    ) -> Optional[MotionController]:
        if Feature.FlowDeck in features:
            return MotionController(self)

        return None

    def _load_multi_ranger(
        self,
        features: set[Feature],
    ) -> Optional[MultiRangerDeck]:
        if Feature.MultiRangerDeck in features:
            return MultiRangerDeck(self)

        return None
