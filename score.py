from settings import *


class Score(Container):
    def __init__(self):
        super().__init__(SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING, BLACK,
                         "bottomright", (
                             WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))

    def run(self):
        self.display_surface.blit(
            self.surface, self.rect)
