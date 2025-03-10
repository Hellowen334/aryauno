import json
import os
from pathlib import Path

RED = "r"
BLUE = "b"
GREEN = "g"
YELLOW = "y"
BLACK = "x"

COLORS = (RED, BLUE, GREEN, YELLOW)

COLOR_ICONS = {RED: "❤️", BLUE: "💙", GREEN: "💚", YELLOW: "💛", BLACK: "⬛️"}

# Values
ZERO = "0"
ONE = "1"
TWO = "2"
THREE = "3"
FOUR = "4"
FIVE = "5"
SIX = "6"
SEVEN = "7"
EIGHT = "8"
NINE = "9"
DRAW_TWO = "draw"
REVERSE = "reverse"
SKIP = "skip"

VALUES = (
    ZERO,
    ONE,
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    DRAW_TWO,
    REVERSE,
    SKIP,
)

# Special cards
CHOOSE = "colorchooser"
DRAW_FOUR = "draw_four"

SPECIALS = (CHOOSE, DRAW_FOUR)

cards = {}
for filename in os.listdir("cards"):
    if filename.endswith(".json"):
        name = filename.split(".")[0]
        try:
            # UTF-8 kodlaması ile dosyayı aç
            with Path(f"cards/{filename}").open(encoding="utf-8") as f:
                cards[name] = json.load(f)
        except UnicodeDecodeError:
            # UTF-8 ile açılamazsa, latin-1 ile dene
            with Path(f"cards/{filename}").open(encoding="latin-1") as f:
                cards[name] = json.load(f)
        except Exception as e:
            print(f"Kart dosyası yüklenirken hata: {filename} - {e}")
