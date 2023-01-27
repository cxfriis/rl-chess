from rl_chess.enums.Enums import Color


class Piece:

    def __init__(self, pos_y: int, pos_x: int, color: Color, short_name="", alive=True):
        self.coords = pos_y, pos_x
        self.color = color
        self.alive = alive
        self.short_name = short_name

    def get_id(self) -> str:
        color_string = "W" if self.color == Color.WHITE else "B"
        return f"{color_string}_{self.short_name}"

    def __str__(self):
        return f"{self.get_id()}: coords={self.coords}"
