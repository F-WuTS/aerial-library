from logging import getLogger
from typing import ContextManager, TYPE_CHECKING, Optional

from cflib.utils.multiranger import Multiranger

from aerial_library.api.errors import RequiredDeckNotFound

if TYPE_CHECKING:
    from aerial_library.backend.drone import Drone


class MultiRangerDeck(ContextManager):
    _log = getLogger(__name__)

    def __init__(self, drone: "Drone"):
        self._drone = drone
        self._deck: Optional[Multiranger] = None

    def __enter__(self):
        self._log.info("Entering")

        if not self._drone.has_deck("bcMultiranger"):
            raise RequiredDeckNotFound("Multi-ranger")

        self._deck = Multiranger(crazyflie=self._drone.cf, rate_ms=10)
        self._deck.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self._log.info("Exiting")

        self._deck.stop()

    def get_front_distance_m(self) -> Optional[float]:
        return self._deck.front

    def get_back_distance_m(self) -> Optional[float]:
        return self._deck.back

    def get_left_distance_m(self) -> Optional[float]:
        return self._deck.left

    def get_right_distance_m(self) -> Optional[float]:
        return self._deck.right

    def get_up_distance_m(self) -> Optional[float]:
        return self._deck.up

    def get_down_distance_m(self) -> Optional[float]:
        return self._deck.down
