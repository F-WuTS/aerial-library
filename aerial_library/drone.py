from typing import Optional, Final

from appdirs import user_cache_dir
from cflib import crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

from aerial_library.droneactions import DroneActions
from aerial_library.util import build_log_config


class Drone:
    """
    Simple, intuitive interface for controlling the Crazyflie 2.1 drone

    Usage example::

        from aerial_library import Drone

        with Drone() as drone:
            drone.takeoff(1.0)

            drone.forward(0.5)
            drone.back(0.5)
            drone.left(0.5)
            drone.right(0.5)

            drone.up(0.5)
            drone.down(0.5)

            drone.turn_left(90)
            drone.turn_right(90)

            drone.land()

    Default speed: 0.25 m/s, 90 deg/s

    Use `fast_mode` (1 m/s, 360 deg/s) only for **well tested** code::

        with Drone(fast_mode=True) as drone:
            ...
    """

    _BATTERY_STATE: Final = {
        0: 'discharging',
        1: 'charging',
        2: 'done charging',
        3: 'low',
        4: 'state #4 "shutdown"'  # TODO figure out meaning
    }

    def __init__(self, fast_mode: bool = False):
        crtp.init_drivers()
        uri = self._select_connection()

        print(f'Connecting to {uri}')
        self._crazyflie = SyncCrazyflie(link_uri=uri, cf=Crazyflie(rw_cache=user_cache_dir(__package__)))

        self._drone_actions: Optional[DroneActions] = None
        self._is_fast_mode = fast_mode

    def __enter__(self) -> DroneActions:
        self._crazyflie.open_link()
        self._display_battery_information()

        m_per_s = 1.0 if self._is_fast_mode else 0.25
        deg_per_s = 180 if self._is_fast_mode else 45
        self._drone_actions = DroneActions(self._crazyflie, m_per_s, deg_per_s)
        return self._drone_actions

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._drone_actions.is_flying:
            self._drone_actions.land()

        self._crazyflie.close_link()

    def _select_connection(self) -> str:
        available = [uri for uri, _ in crtp.scan_interfaces()]

        match len(available):
            case 0:
                raise RuntimeError('Cannot choose connection: No connections available')

            case 1:
                return available[0]

            case 2:
                index = self._ask_desired_connection(available)
                return available[index]

    def _display_battery_information(self):
        log_config = build_log_config(
            'Battery Information',
            1000,
            (
                'pm.batteryLevel',
                'pm.state'
            )
        )

        with SyncLogger(self._crazyflie, log_config) as log:
            data = log.next()[1]
            percentage = data['pm.batteryLevel']
            state_id = data['pm.state']
            print(f'Battery is {Drone._BATTERY_STATE[state_id]} at {percentage}%')

    @staticmethod
    def _ask_desired_connection(available) -> int:
        print('Multiple connections available:')
        for i, option in enumerate(available):
            print(f'-> {i}: {option}')

        choice: Optional[int] = None
        while (choice is None
               or choice not in range(len(available))):
            try:
                in_str = input('Enter connection number: ')
                choice = int(in_str)

            except ValueError:
                pass

        return choice
