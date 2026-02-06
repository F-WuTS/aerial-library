from aerial_library.backend.motioncontroller import MotionController


class Move:
    def __init__(self, backend: MotionController):
        self._backend = backend

    @property
    def is_flying(self) -> bool:
        return self._backend.is_flying

    def takeoff(self, height_m: float) -> None:
        self._backend.takeoff(height_m)

    def land(self) -> None:
        self._backend.land()

    def forward(self, distance_m: float) -> None:
        self.move(forward=distance_m)

    def back(self, distance_m: float) -> None:
        self.move(back=distance_m)

    def left(self, distance_m: float) -> None:
        self.move(left=distance_m)

    def right(self, distance_m: float) -> None:
        self.move(right=distance_m)

    def up(self, distance_m: float) -> None:
        self.move(up=distance_m)

    def down(self, distance_m: float) -> None:
        self.move(down=distance_m)

    def turn_left(self, angle_deg: float) -> None:
        self.move(turn_left=angle_deg)

    def turn_right(self, angle_deg: float) -> None:
        self.move(turn_right=angle_deg)

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
    ) -> None:
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
