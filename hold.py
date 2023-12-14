from settings import *


class Hold(Container):
    def __init__(self):
        super().__init__(SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION, BLACK,
                         "topleft", (
                             PADDING, PADDING))

    def run(self):
        self.display_surface.blit(
            self.surface, self.rect)
