from .coordinate import Coordinate
from .debounce import debounce
from .hitbox import Hitbox
import pyautogui

instrument_to_key = {
    "hi hat": "4",
    "ride bell": "8",
    "crash": "9",
    "ride": "7",
    "tom 1": "Q",
    "tom 2": "W",
    "snare": "2",
    "floor tom": "E",
}


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
        pyautogui.press(instrument_to_key[self.name])
        print(f"Playing the ${self.name}: {self.sound}")
