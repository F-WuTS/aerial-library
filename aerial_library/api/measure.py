from math import inf as infinity

from aerial_library.backend.multirangerdeck import MultiRangerDeck


class Measure:
    def __init__(self, backend: MultiRangerDeck):
        self._backend = backend

    def front(self) -> float:
        return self._backend.get_front_distance_m() or infinity

    def back(self) -> float:
        return self._backend.get_back_distance_m() or infinity

    def left(self) -> float:
        return self._backend.get_left_distance_m() or infinity

    def right(self) -> float:
        return self._backend.get_right_distance_m() or infinity

    def up(self) -> float:
        return self._backend.get_up_distance_m() or infinity

    def down(self) -> float:
        return self._backend.get_down_distance_m() or infinity
