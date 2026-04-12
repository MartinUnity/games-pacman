import os

from .constants import HIGHSCORE_FILE


def load_highscore():
    """Load highscore from file, returns 0 if file doesn't exist"""
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                score = int(f.read().strip())
                return score
    except (ValueError, IOError):
        pass
    return 0


def save_highscore(score):
    """Save highscore to file"""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except IOError:
        pass
