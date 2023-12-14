from settings import *


class Preview(Container):
    def __init__(self):
        super().__init__(SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION, BLACK,
                         "topright", (
                             WINDOW_WIDTH - PADDING, PADDING))

    def run(self):
        self.display_surface.blit(
            self.surface, self.rect)
