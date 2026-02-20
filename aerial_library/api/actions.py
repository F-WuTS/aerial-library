from math import inf as infinity

from aerial_library.api.errors import MissingFeature
from aerial_library.api.feature import Feature, FlowDeck, MultiRangerDeck
from aerial_library.backend.drone import Drone


class Actions:
    """This class contains the functions that can be used on a connected Drone.

    Activating a Drone using a `with`-statement returns an instance of this class:

    >>> from aerial_library import Drone
    >>>
    >>> with Drone("E7E7E7E7E7") as drone:
    ...     print(type(drone))  # "<class aerial_library.api.actions.Actions>"
    """

    def __init__(self, features: set[Feature], backend: Drone):
        self._features = features
        self._backend = backend

    def get_battery_level(self) -> float:
        """Returns the battery level of the drone as a percentage.

        The percentage is rounded to the nearest 10%.

        The battery is considered full at 90%.
        It is advised to always use a full battery for an extended flight.
        """
        level = self._backend.battery_level
        return level

    def takeoff(self, height: float):
        """Take off to the given height in meters.

        This requires the `FlowDeck` feature.

        The drone will always take off quickly to a fixed height.
        It then corrects its position and ascends or descends to the desired height.
        """
        print(f"Taking off to {height}m")
        self._require_feature(FlowDeck)
        self._backend.motion_controller.takeoff(height)

    def land(self):
        """Lands the drone.

        This requires the `FlowDeck` feature.

        The drone will fall down the last few centimeters
        to avoid drifting sideways near the ground.
        """
        print("Landing")
        self._require_feature(FlowDeck)
        self._backend.motion_controller.land()

    def move_forward(self, distance: float):
        """Move forward by the given distance in meters.

        This requires the `FlowDeck` feature.
        """
        print(f"Moving forward by {distance}m")
        self._require_feature(FlowDeck)
        self._move(forward=distance)

    def move_back(self, distance: float):
        """Move back by the given distance in meters.

        This requires the `FlowDeck` feature.
        """
        print(f"Moving back by {distance}m")
        self._require_feature(FlowDeck)
        self._move(back=distance)

    def move_left(self, distance: float):
        """Move left by the given distance in meters.

        This requires the `FlowDeck` feature.
        """
        print(f"Moving left by {distance}m")
        self._require_feature(FlowDeck)
        self._move(left=distance)

    def move_right(self, distance: float):
        """Move right by the given distance in meters.

        This requires the `FlowDeck` feature.
        """
        print(f"Moving right by {distance}m")
        self._require_feature(FlowDeck)
        self._move(right=distance)

    def move_up(self, distance: float):
        """Ascend by the given distance in meters.

        This requires the `FlowDeck` feature.
        """
        print(f"Moving up by {distance}m")
        self._require_feature(FlowDeck)
        self._move(up=distance)

    def move_down(self, distance: float):
        """Descend by the given distance in meters.

        This requires the `FlowDeck` feature.
        """
        print(f"Moving down by {distance}m")
        self._require_feature(FlowDeck)
        self._move(down=distance)

    def turn_left(self, angle: float):
        """Turns the drone to the left by the given angle in degrees.

        This requires the `FlowDeck` feature.
        """
        print(f"Turning left by {angle}°")
        self._require_feature(FlowDeck)
        self._move(turn_left=angle)

    def turn_right(self, angle: float):
        """Turns the drone to the right by the given angle in degrees.

        This requires the `FlowDeck` feature.
        """
        print(f"Turning right by {angle}°")
        self._require_feature(FlowDeck)
        self._move(turn_right=angle)

    def move(
        self,
        forward: float = 0,
        back: float = 0,
        left: float = 0,
        right: float = 0,
        up: float = 0,
        down: float = 0,
        turn_left: float = 0,
        turn_right: float = 0,
    ):
        """Moves the drone by the given parameters.

        This requires the `FlowDeck` feature.

        Diagonal movement as well as spinning while moving is thereby supported.

        Example:
        >>> from aerial_library import Drone, FlowDeck
        >>>
        >>> with Drone("E7E7E7E7E7", FlowDeck) as drone:
        ...     drone.takeoff(0.5)
        ...     drone.move(forward=1.0, up=0.5)
        """
        lateral = {
            "forward": forward,
            "back": back,
            "left": left,
            "right": right,
            "up": up,
            "down": down,
        }
        rotational = {
            "turn_left": turn_left,
            "turn_right": turn_right,
        }

        print(f"Moving by custom parameters:")

        for param, value in lateral.items():
            print(f"  {param}: {value}m")

        for param, value in rotational.items():
            print(f"  {param}: {value}°")

        self._move(forward, back, left, right, up, down, turn_left, turn_right)

    def set_fast_mode(self, enable: bool):
        """Enables or disables fast mode, which makes the drone move and turn a lot faster.

        This requires the `FlowDeck` feature.

        By default, fast mode is disabled.
        Turning on fast mode does not affect takeoff and landing.
        """
        print(f"{'Enabling' if enable else 'Disabling'} fast mode")
        self._require_feature(FlowDeck)
        self._backend.motion_controller.set_fast_mode(enable)

    def measure_front(self) -> float:
        """Returns the distance to the obstacle in front of the drone in meters.

        This requires the `MultiRangerDeck` feature.

        Returns infinity if no obstacle is detected.
        """
        self._require_feature(MultiRangerDeck)
        return self._backend.multi_ranger.get_front_distance_m() or infinity

    def measure_back(self) -> float:
        """Returns the distance to the obstacle behind the drone in meters.

        This requires the `MultiRangerDeck` feature.

        Returns infinity if no obstacle is detected.
        """
        self._require_feature(MultiRangerDeck)
        return self._backend.multi_ranger.get_back_distance_m() or infinity

    def measure_left(self) -> float:
        """Returns the distance to the obstacle to the left of the drone in meters.

        This requires the `MultiRangerDeck` feature.

        Returns infinity if no obstacle is detected.
        """
        self._require_feature(MultiRangerDeck)
        return self._backend.multi_ranger.get_left_distance_m() or infinity

    def measure_right(self) -> float:
        """Returns the distance to the obstacle to the right of the drone in meters.

        This requires the `MultiRangerDeck` feature.

        Returns infinity if no obstacle is detected.
        """
        self._require_feature(MultiRangerDeck)
        return self._backend.multi_ranger.get_right_distance_m() or infinity

    def measure_up(self) -> float:
        """Returns the distance to the obstacle above the drone in meters.

        This requires the `MultiRangerDeck` feature.

        Returns infinity if no obstacle is detected.
        """
        self._require_feature(MultiRangerDeck)
        return self._backend.multi_ranger.get_up_distance_m() or infinity

    def measure_down(self) -> float:
        """Returns the distance to the ground or other obstacle below the drone in meters.

        This requires the `MultiRangerDeck` feature and the `FlowDeck` feature,
        because the sensor for measuring downwards is located on the Flow Deck.

        Returns infinity if no obstacle is detected or the Flow Deck is not attached.
        """
        self._require_feature(MultiRangerDeck)
        self._require_feature(FlowDeck)
        return self._backend.multi_ranger.get_down_distance_m() or infinity

    def _require_feature(self, feature: Feature):
        if feature not in self._features:
            raise MissingFeature(feature)

    def _move(
        self,
        forward: float = 0,
        back: float = 0,
        left: float = 0,
        right: float = 0,
        up: float = 0,
        down: float = 0,
        turn_left: float = 0,
        turn_right: float = 0,
    ):
        total_forward = forward - back
        total_left = left - right
        total_up = up - down
        total_yaw = turn_left - turn_right

        self._backend.motion_controller.change_relative_position(
            forward_m=total_forward,
            left_m=total_left,
            up_m=total_up,
            yaw_deg=total_yaw,
        )
