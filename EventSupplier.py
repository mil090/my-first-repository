from enum import Enum, auto
class PitchResult(Enum):
    BALL=auto()
    CALLED_STRIKE=auto()
    SWINGING_STRIKE=auto()
    FOUL=auto()
    IN_PLAY=auto()
    HBP=auto()
    WP=auto()
    BALK=auto()