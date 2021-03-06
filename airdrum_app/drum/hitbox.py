from abc import ABC, abstractmethod

from . import Coordinate


class Hitbox(ABC):
    @abstractmethod
    def is_colliding(self, coordinate: Coordinate) -> bool:
        pass
