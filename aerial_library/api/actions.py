from aerial_library.api.errors import MissingFeature
from aerial_library.api.feature import Feature
from aerial_library.api.measure import Measure
from aerial_library.api.move import Move
from aerial_library.backend.drone import Drone


class Actions:
    def __init__(self, features: set[Feature], backend: Drone):
        self._features = features

        self._move = Move(backend.motion_controller) if backend.motion_controller else None
        self._measure = Measure(backend.multi_ranger) if backend.multi_ranger else None

    @property
    def move(self) -> Move:
        if Feature.FlowDeck not in self._features:
            raise MissingFeature(Feature.FlowDeck, "move")

        return self._move

    @property
    def measure(self) -> Measure:
        if Feature.MultiRangerDeck not in self._features:
            raise MissingFeature(Feature.MultiRangerDeck, "measure")

        return self._measure
