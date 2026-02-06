from typing import ContextManager, TYPE_CHECKING

from aerial_library.api.errors import MultiRangerDeckNotFound

if TYPE_CHECKING:
    from aerial_library.backend.drone import Drone


class MultiRangerDeck(ContextManager):
    def __init__(self, drone: "Drone"):
        self._drone = drone

    def __enter__(self):
        if not self._drone.has_deck("bcMultiranger"):
            raise MultiRangerDeckNotFound()

    def __exit__(self, exc_type, exc_value, traceback, /):
        pass
