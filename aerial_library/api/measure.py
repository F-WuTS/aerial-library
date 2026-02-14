from math import inf as infinity

from aerial_library.backend.multirangerdeck import MultiRangerDeck


class Measure:
    def __init__(self, backend: MultiRangerDeck):
        self._backend = backend

    def front(self) -> float:
        """Returns the distance to the obstacle in front of the drone in meters.

        Returns infinity if no obstacle is detected.
        """
        return self._backend.get_front_distance_m() or infinity

    def back(self) -> float:
        """Returns the distance to the obstacle behind the drone in meters.

        Returns infinity if no obstacle is detected.
        """
        return self._backend.get_back_distance_m() or infinity

    def left(self) -> float:
        """Returns the distance to the obstacle to the left of the drone in meters.

        Returns infinity if no obstacle is detected.
        """
        return self._backend.get_left_distance_m() or infinity

    def right(self) -> float:
        """Returns the distance to the obstacle to the right of the drone in meters.

        Returns infinity if no obstacle is detected.
        """
        return self._backend.get_right_distance_m() or infinity

    def up(self) -> float:
        """Returns the distance to the obstacle above the drone in meters.

        Returns infinity if no obstacle is detected.
        """
        return self._backend.get_up_distance_m() or infinity

    def down(self) -> float:
        """Returns the distance to the ground or other obstacle below the drone in meters.

        The sensor for measuring downwards is located on the Flow Deck,
        so the Flow Deck must be attached for this to work.

        Returns infinity if no obstacle is detected or the Flow Deck is not attached.
        """
        return self._backend.get_down_distance_m() or infinity
