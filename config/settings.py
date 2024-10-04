from dataclasses import dataclass

@dataclass
class Window:
    screenSize: tuple = (900, 900)
    cellSize: int = 7

@dataclass
class Colors:
    color_white = (255, 255, 255)
    color_red = (255, 0, 0)
    color_green = (0, 255, 0)
    color_grey = (120, 120, 120)
    color_line = (80, 80, 80)
    color_path = (195, 195, 90)
    color_frame = (230, 210, 181)

    color_blue = (0, 255, 255) # Start cell
    color_purple = (139, 0, 255) # End cell

window_config = Window()
color_config = Colors()
