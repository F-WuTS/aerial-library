from math import sqrt
from typing import Self


class Position:
    def __init__(self, x: float, y: float, z: float, yaw: float):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw

    def distance_to(self, other: Self) -> float:
        return sqrt(
            pow(self.x - other.x, 2)
            + pow(self.y - other.y, 2)
            + pow(self.z - other.z, 2)
        )

    def angle_to(self, other: Self) -> float:
        diff = (self.yaw - other.yaw + 180) % 360 - 180
        return abs(diff)

    def copy(self) -> Self:
        return Position(self.x, self.y, self.z, self.yaw)

    def __str__(self) -> str:
        return f"(x: {self.x:2.4f}, y: {self.y:2.4f}, z: {self.z:2.4f}, yaw: {self.yaw:2.4f})"
