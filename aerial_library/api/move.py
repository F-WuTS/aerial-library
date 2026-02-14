from aerial_library.backend.motioncontroller import MotionController


class Move:
    def __init__(self, backend: MotionController):
        self._backend = backend

    @property
    def is_flying(self) -> bool:
        """Returns whether the drone should currently be flying.

        Example:
            >>> from aerial_library import Drone, FlowDeck
            >>>
            >>> with Drone("E7E7E7E7E7", FlowDeck) as drone:
            ...     print(drone.move.is_flying)  # False
            ...
            ...     drone.move.takeoff(1.0)
            ...     print(drone.move.is_flying)  # True
            ...
            ...     drone.move.land()
            ...     print(drone.move.is_flying)  # False
        """
        return self._backend.is_flying

    def takeoff(self, height_m: float):
        """Take off to a given height.

        The drone will always take off quickly to a fixed height.
        Then it corrects its position and ascends or descends to the desired height.
        """
        print(f"Taking off to {height_m} m")
        self._backend.takeoff(height_m)

    def land(self):
        """Lands the drone.

        The drone will fall down the last few centimeters to avoid drifting sideways near the ground.
        """
        print("Landing")
        self._backend.land()

    def forward(self, distance_m: float):
        """Moves the drone forward by the given distance."""
        print(f"Moving forward by {distance_m} m")
        self._move(forward=distance_m)

    def back(self, distance_m: float):
        """Moves the drone backward by the given distance."""
        print(f"Moving back by {distance_m} m")
        self._move(back=distance_m)

    def left(self, distance_m: float):
        """Moves the drone to the left by the given distance."""
        print(f"Moving left by {distance_m} m")
        self._move(left=distance_m)

    def right(self, distance_m: float):
        """Moves the drone to the right by the given distance."""
        print(f"Moving right by {distance_m} m")
        self._move(right=distance_m)

    def up(self, distance_m: float):
        """Makes the drone ascend by the given distance."""
        print(f"Moving up by {distance_m} m")
        self._move(up=distance_m)

    def down(self, distance_m: float):
        """Makes the drone descend by the given distance."""
        print(f"Moving down by {distance_m} m")
        self._move(down=distance_m)

    def turn_left(self, angle_deg: float):
        """Turns the drone to the left by the given angle."""
        print(f"Turning left by {angle_deg}°")
        self._move(turn_left=angle_deg)

    def turn_right(self, angle_deg: float):
        """Turns the drone to the right by the given angle."""
        print(f"Turning right by {angle_deg}°")
        self._move(turn_right=angle_deg)

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

        Example:
            >>> from aerial_library import Drone, FlowDeck
            >>>
            >>> with Drone("E7E7E7E7E7", FlowDeck) as drone:
            ...     drone.move.takeoff(0.5)
            ...     drone.move.move(forward=1.0, up=0.5)
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

        print(f"Moving by custom values:")

        for param, value in lateral.items():
            print(f"  {param}: {value} m")

        for param, value in rotational.items():
            print(f"  {param}: {value} °")

        self._move(forward, back, left, right, up, down, turn_left, turn_right)

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

        self._backend.change_relative_position(
            forward_m=total_forward,
            left_m=total_left,
            up_m=total_up,
            yaw_deg=total_yaw,
        )
