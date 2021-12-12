from .coordinate import Coordinate
from .hitbox import Hitbox


class CircularHitbox(Hitbox):
    center_x: int  # Center of the circle
    center_y: int
    r: int  # Radius of the circle

    def __init__(self, center: Coordinate, radius: int):
        self.center_x, self.center_y = center
        self.r = radius

    def is_colliding(self, coordinate: Coordinate) -> bool:
        x, y = coordinate
        return (x - self.center_x)**2 + (y - self.center_y)**2 <= self.r**2
