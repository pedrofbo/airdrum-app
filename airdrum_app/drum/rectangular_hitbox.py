from . import Coordinate
from .hitbox import Hitbox


class RectangularHitbox(Hitbox):
    x0: int  # Top left X coordinate
    y0: int  # Top left Y coordinate
    x1: int  # Bottom right X coordinate
    y1: int  # Bottom right Y coordinate

    def __init__(self, top_left: Coordinate, bottom_right: Coordinate):
        self.x0, self.y0 = top_left
        self.x1, self.y1 = bottom_right

    def is_colliding(self, coordinate: Coordinate) -> bool:
        x, y = coordinate
        return (self.x0 < x < self.x1) and (self.y0 < y < self.y1)
