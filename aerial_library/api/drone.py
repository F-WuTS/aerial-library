from typing import ContextManager

from cflib import crtp

from aerial_library.api.actions import Actions
from aerial_library.api.feature import Feature
from aerial_library.backend.drone import Drone as DroneBackend
from aerial_library.backend.util import select_connection


class Drone(ContextManager):
    """`Drone` is your entrypoint to programming your Crazyflie drone.

    Instantiate the `Drone` in a `with`-statement.
    First, specify the radio address of your Crazyflie.
    Then, declare the `Features` you would like to use, for example `FlowDeck`.
    The returned object should be named and can then be used to control the drone:

    >>> from aerial_library import Drone, FlowDeck
    >>>
    >>> with Drone("E7E7E7E7E7", FlowDeck) as minidrone:
    ...     minidrone.takeoff(1.0)

    This context manager will take care of almost everything:

    * When running the `with`-block, the user is first asked which drone to connect to.
      If no drones are found, an error will be raised.

    * Once connected, the additional features are loaded and the drone is checked for the required hardware.
      The battery state is displayed in the terminal for manual checking.

    * Now the code inside the `with`-block is executed.
      At the end of the `with`-block, the drone is automatically landed if necessary.
      This is also the case should the program raise an error while the drone is flying.
      After landing, the Crazyflie is disconnected.

    Example:
        This short script connects to a Crazyflie with all features enabled.
        The drone takes off to an altitude of 1 meter and measures the distance to the front:

        >>> from aerial_library import Drone, FlowDeck, MultiRangerDeck
        >>>
        >>> with Drone(
        ...     "E7E7E7E7E7",
        ...     FlowDeck,
        ...     MultiRangerDeck,
        ... ) as drone:
        ...     drone.takeoff(1.0)
        ...
        ...     distance = drone.measure_front()
        ...     print(f"Distance to front in meters: {distance}")
    """

    def __init__(
        self,
        address: str,
        *features: Feature,
    ):
        print(f"Looking for drones with address {address}")

        crtp.init_drivers()
        uri = select_connection(address)

        self._features = set(features)
        self._backend = DroneBackend(uri, self._features)

    def __enter__(self) -> Actions:
        print("Starting drone program")
        self._backend.__enter__()
        self._display_battery_state()

        return Actions(self._features, self._backend)

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting drone program")
        self._backend.__exit__(exc_type, exc_value, traceback)

    def _display_battery_state(self):
        state = self._backend.battery_state
        level = self._backend.battery_level
        print(f"Battery is {state} at {level}%")
