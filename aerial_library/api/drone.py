from typing import ContextManager

from cflib import crtp

from aerial_library.api.actions import Actions
from aerial_library.api.feature import Feature
from aerial_library.backend.drone import Drone as PhysicalDrone
from aerial_library.backend.util import select_connection


class Drone(ContextManager):
    """ "Drone" is your entrypoint to programming your Crazyflie drone, intended to be used in a with-statement.

    This class will take care of almost everything.
    The user can focus on the actual logic code without distractions:

    When running the with-block, the user is first asked which drone to connect to.
    If only one drone is found, that drone will be used automatically.
    If no drones are found, an error will be raised.

    Once connected, the code inside the with-block is run.
    The ``move`` and ``measure`` APIs can be used here to control the drone.

    At the end of the with-block, the drone is automatically landed if necessary.
    This is also the case should the program raise an error while the drone is flying.
    After landing, the Crazyflie is disconnected.

    Example:
        Here is a short example script that connects to a Crazyflie with all features enabled.
        The drone takes off at an altitude of 1 meter and measures the distance to the front:

        >>> from aerial_library import Drone, FlowDeck, MultiRangerDeck, FastMode
        >>>
        >>> with Drone(
        ...    FlowDeck,
        ...    MultiRangerDeck,
        ...    FastMode,
        ... ) as drone:
        ...    drone.move.takeoff(1.0)
        ...
        ...    distance = drone.measure.front()
        ...    print(f"Distance to front in meters: {distance}")

    """

    def __init__(self, *features: Feature):
        crtp.init_drivers()
        uri = select_connection()

        self._features = set(features)
        self._backend = PhysicalDrone(uri, self._features)

    def __enter__(self) -> Actions:
        self._backend.__enter__()
        self._display_battery_state()

        return Actions(self._features, self._backend)

    def __exit__(self, exc_type, exc_value, traceback):
        self._backend.__exit__(exc_type, exc_value, traceback)

    def _display_battery_state(self):
        state, level = self._backend.get_battery_information()
        print(f"Battery state: {state.name} at {level}%")
