from aerial_library.backend.motioncontroller import MotionController


class Move:
    def __init__(self, backend: MotionController):
        self._backend = backend

    @property
    def is_flying(self) -> bool:
        return self._backend.is_flying

    def takeoff(self, height_m: float):
        print(f"Taking off to {height_m} m")
        self._backend.takeoff(height_m)

    def land(self):
        print("Landing")
        self._backend.land()

    def forward(self, distance_m: float):
        print(f"Moving forward by {distance_m} m")
        self._move(forward=distance_m)

    def back(self, distance_m: float):
        print(f"Moving back by {distance_m} m")
        self._move(back=distance_m)

    def left(self, distance_m: float):
        print(f"Moving left by {distance_m} m")
        self._move(left=distance_m)

    def right(self, distance_m: float):
        print(f"Moving right by {distance_m} m")
        self._move(right=distance_m)

    def up(self, distance_m: float):
        print(f"Moving up by {distance_m} m")
        self._move(up=distance_m)

    def down(self, distance_m: float):
        print(f"Moving down by {distance_m} m")
        self._move(down=distance_m)

    def turn_left(self, angle_deg: float):
        print(f"Turning left by {angle_deg}°")
        self._move(turn_left=angle_deg)

    def turn_right(self, angle_deg: float):
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
