from abc import ABC, abstractmethod


class Hitbox(ABC):
    @abstractmethod
    def is_colliding(self, coordinate) -> bool:
        pass
