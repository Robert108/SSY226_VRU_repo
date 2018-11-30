class Colors:
    "Represents colors as a list of ['red', 'green', 'blue'] integers (0-255)"

    @property
    def WHITE(self):
        return [255, 255, 255]

    @property
    def BLACK(self):
        return [0, 0, 0]

    @property
    def RED(self):
        return [255, 0, 0]

    @property
    def GREEN(self):
        return [0, 255, 0]

    @property
    def YELLOW(self):
        return [255, 255, 0]


class PixelSymbols:
    "8x8 RGB pixel 'art'"

    @property
    def WARNING_LEFT(self, background=Colors().BLACK, foreground=Colors().RED):
        "Indicates a warning to the left of the display"
        _ = background
        O = foreground

        return [
            _, _, _, O, _, _, _, _,
            _, _, O, _, _, O, _, _,
            _, O, _, _, _, O, _, _,
            O, _, _, _, _, O, _, _,
            O, _, _, _, _, O, _, _,
            _, O, _, _, _, _, _, _,
            _, _, O, _, _, O, _, _,
            _, _, _, O, _, _, _, _
        ]

    @property
    def WARNING_RIGHT(self, background=Colors().BLACK, foreground=Colors().RED):
        "Indicates a warning to the right of the display"
        _ = background
        O = foreground

        return [
            _, _, _, _, O, _, _, _,
            _, _, O, _, _, O, _, _,
            _, _, O, _, _, _, O, _,
            _, _, O, _, _, _, _, O,
            _, _, O, _, _, _, _, O,
            _, _, _, _, _, _, O, _,
            _, _, O, _, _, O, _, _,
            _, _, _, _, O, _, _, _
        ]

    @property
    def WARNING_DOWN(self, background=Colors().BLACK, foreground=Colors().RED):
        "Indicates a warning below the display"
        _ = background
        O = foreground

        return [
            _, _, _, _, _, _, _, _,
            _, _, _, O, O, _, _, _,
            _, _, _, O, O, _, _, _,
            _, _, _, O, O, _, _, _,
            O, _, _, _, _, _, _, O,
            _, O, _, O, O, _, O, _,
            _, _, O, _, _, O, _, _,
            _, _, _, O, O, _, _, _
        ]

    @property
    def WARNING_UP(self, background=Colors().BLACK, foreground=Colors().RED):
        "Indicates a warning above the display"
        _ = background
        O = foreground

        return [
            _, _, _, O, O, _, _, _,
            _, _, O, _, _, O, _, _,
            _, O, _, _, _, _, O, _,
            O, _, _, O, O, _, _, O,
            _, _, _, O, O, _, _, _,
            _, _, _, O, O, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, O, O, _, _, _
        ]

    @property
    def WARNING_STATIONARY(self, background=Colors().BLACK, foreground=Colors().RED):
        "Indicates a warning above the display"
        _ = background
        O = foreground

        return [
            _, O, O, O, O, O, O, _,
            O, _, _, _, _, _, _, O,
            O, _, _, _, _, _, _, O,
            O, _, _, _, _, _, _, O,
            O, _, _, _, _, _, _, O,
            O, _, _, _, _, _, _, O,
            O, _, _, _, _, _, _, O,
            _, O, O, O, O, O, O, _
        ]

    @property
    def BLANK(self, background=Colors().BLACK):
        "Sets all pixels to the same color (self, default black)"
        _ = background

        return [
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _,
            _, _, _, _, _, _, _, _
        ]
