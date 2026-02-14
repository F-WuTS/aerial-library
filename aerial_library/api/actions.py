from aerial_library.api.errors import MissingFeature
from aerial_library.api.feature import Feature
from aerial_library.api.measure import Measure
from aerial_library.api.move import Move
from aerial_library.backend.drone import Drone


class Actions:
    def __init__(self, features: set[Feature], backend: Drone):
        self._features = features

        move_backend = backend.motion_controller
        measure_backend = backend.multi_ranger

        self._move = Move(move_backend) if move_backend else None
        self._measure = Measure(measure_backend) if measure_backend else None

    @property
    def move(self) -> Move:
        """Functions on the `move` API are used to control the drone's motion.

        This requires the `FlowDeck` feature.

        Example:
            >>> from aerial_library import Drone, FlowDeck
            >>>
            >>> with Drone("E7E7E7E7E7", FlowDeck) as drone:
            ...     drone.move.takeoff(0.7)
            ...     drone.move.forward(1.2)
        """
        if Feature.FlowDeck not in self._features:
            raise MissingFeature(Feature.FlowDeck, "move")

        return self._move

    @property
    def measure(self) -> Measure:
        """Functions on the `measure` API are used to measure distances to objects around the drone.

        This requires the `MultiRangerDeck` feature.

        Example:
            >>> from aerial_library import Drone, MultiRangerDeck
            >>>
            >>> with Drone("E7E7E7E7E7", MultiRangerDeck) as drone:
            ...     distance = drone.measure.front()
            ...     print(f"Distance to the thing in front of the drone: {distance} meter")
        """
        if Feature.MultiRangerDeck not in self._features:
            raise MissingFeature(Feature.MultiRangerDeck, "measure")

        return self._measure
