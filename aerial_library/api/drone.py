from typing import ContextManager

from cflib import crtp

from aerial_library.api.actions import Actions
from aerial_library.api.feature import Feature
from aerial_library.backend.drone import Drone as PhysicalDrone
from aerial_library.backend.util import select_connection


class Drone(ContextManager):
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
