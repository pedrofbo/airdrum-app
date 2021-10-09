from . import Coordinate
from .debounce import debounce
from .hitbox import Hitbox


class DrumComponent:
    name: str
    sound: str
    hitbox: Hitbox

    def __init__(self, name: str, sound: str, hitbox: Hitbox):
        self.name = name
        self.sound = sound
        self.hitbox = hitbox

    def is_hit(self, coordinate: Coordinate) -> bool:
        return self.hitbox.is_colliding(coordinate)

    @debounce(timeout_ms=1000)
    def play_sound(self) -> None:
        print(f"Playing the ${self.name}: {self.sound}")
