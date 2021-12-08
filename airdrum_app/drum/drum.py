from . import Coordinate
from .drum_component import DrumComponent
from .circular_hitbox import CircularHitbox


class Drum:
    components: list[DrumComponent]

    def __init__(self):
        self._init_components()

    def _init_components(self):
        self.components = [
            DrumComponent("hi hat", "hi_hat.midi", CircularHitbox((135, 465), 104)),
            DrumComponent("crash", "crash.midi", CircularHitbox((233, 280), 102)),
            DrumComponent("ride bell", "ride_bell.midi", CircularHitbox((660, 280), 51)),
            DrumComponent("ride", "ride.midi", CircularHitbox((775, 395), 104)),
            DrumComponent("snare", "snare.midi", CircularHitbox((310, 550), 87)),
            DrumComponent("floor tom", "floor_tom.midi", CircularHitbox((650, 565), 106)),
            DrumComponent("tom 1", "tom_1.midi", CircularHitbox((395, 358), 73)),
            DrumComponent("tom 2", "tom_2.midi", CircularHitbox((548, 358), 73)),
        ]

        # self.components = [
        #     DrumComponent("ride", "ride.midi", RectangularHitbox((0, 0), (200, 150))),
        #     DrumComponent("ride bell", "ride_bell.midi", RectangularHitbox((210, 0), (430, 150))),
        #     DrumComponent("hit hat close", "hit_hat_close.midi", RectangularHitbox((440, 0), (650, 150))),
        #     DrumComponent("crash", "crash.midi", RectangularHitbox((660, 0), (900, 150))),
        #     DrumComponent("snare", "snare.midi", RectangularHitbox((0, 160), (50, 370))),
        #     DrumComponent("snare rim", "snare_rim.midi", RectangularHitbox((0, 380), (50, 570))),
        #     DrumComponent("hit hat", "hit_hat.midi", RectangularHitbox((850, 160), (900, 370))),
        #     DrumComponent("hit hat open", "hit_hat_open.midi", RectangularHitbox((850, 380), (900, 570))),
        #     DrumComponent("tom hi", "tom_hi.midi", RectangularHitbox((0, 580), (200, 700))),
        #     DrumComponent("tom mid", "tom_mid.midi", RectangularHitbox((210, 580), (430, 700))),
        #     DrumComponent("tom low", "tom_low.midi", RectangularHitbox((440, 580), (650, 700))),
        #     DrumComponent("hit hat open", "hit_hat_open.midi", RectangularHitbox((660, 580), (900, 700))),
        # ]

    def hit(self, coordinate: Coordinate) -> None:
        for component in self.components:
            if component.is_hit(coordinate):
                component.play_sound()
                break
