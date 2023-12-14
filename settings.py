import pygame

# Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 30
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# side bar size
SIDEBAR_WIDTH = 150
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH * 2 + 3 * PADDING
WINDOW_HEIGHT = GAME_HEIGHT + 2 * PADDING

# game behavior
UPDATE_START_SPEED = 500
MOVE_WAIT_TIME = 100
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS/2, -1)

# colors
YELLOW = '#f1e60d'
RED = '#e80c0c'
LIGHT_BLUE = '#0ce8e8'
DARK_BLUE = '#0c0ce8'
GREEN = '#0ce80c'
ORANGE = '#ff6600'
WHITE = '#ffffff'
BLACK = '#000000'
MAGENTA = '#ff00ff'
GRAY = '#808080'
LINE_COLOR = '#ffffff'

# shapes
TETROMINOS = {
    'T': {
        'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color': MAGENTA
    },
    'S': {
        'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': GREEN
    },
    'Z': {
        'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': RED
    },
    'J': {
        'shape': [(0, 0), (-1, 0), (1, 0), (-1, -1)], 'color': DARK_BLUE
    },
    'L': {
        'shape': [(0, 0), (-1, 0), (1, 0), (1, -1)], 'color': ORANGE
    },
    'I': {
        'shape': [(0, 0), (-1, 0), (1, 0), (2, 0)], 'color': LIGHT_BLUE
    },
    'O': {
        'shape': [(0, 0), (1, 0), (0, -1), (1, -1)], 'color': YELLOW
    },
}

# offsets data
JLSTZ_OFFSET_DATA = [[pygame.Vector2() for x in range(4)] for y in range(5)]
JLSTZ_OFFSET_DATA[0][0] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[0][1] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[0][2] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[0][3] = pygame.Vector2(0, 0)

JLSTZ_OFFSET_DATA[1][0] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[1][1] = pygame.Vector2(1, 0)
JLSTZ_OFFSET_DATA[1][2] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[1][3] = pygame.Vector2(-1, 0)

JLSTZ_OFFSET_DATA[2][0] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[2][1] = pygame.Vector2(1, -1)
JLSTZ_OFFSET_DATA[2][2] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[2][3] = pygame.Vector2(-1, -1)

JLSTZ_OFFSET_DATA[3][0] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[3][1] = pygame.Vector2(0, 2)
JLSTZ_OFFSET_DATA[3][2] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[3][3] = pygame.Vector2(0, 2)

JLSTZ_OFFSET_DATA[4][0] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[4][1] = pygame.Vector2(1, 2)
JLSTZ_OFFSET_DATA[4][2] = pygame.Vector2(0, 0)
JLSTZ_OFFSET_DATA[4][3] = pygame.Vector2(-1, 2)

# I offset data
I_OFFSET_DATA = [[pygame.Vector2() for x in range(4)] for y in range(5)]
I_OFFSET_DATA[0][0] = pygame.Vector2(0, 0)
I_OFFSET_DATA[0][1] = pygame.Vector2(-1, 0)
I_OFFSET_DATA[0][2] = pygame.Vector2(-1, 1)
I_OFFSET_DATA[0][3] = pygame.Vector2(0, 1)

I_OFFSET_DATA[1][0] = pygame.Vector2(-1, 0)
I_OFFSET_DATA[1][1] = pygame.Vector2(0, 0)
I_OFFSET_DATA[1][2] = pygame.Vector2(1, 1)
I_OFFSET_DATA[1][3] = pygame.Vector2(0, 1)

I_OFFSET_DATA[2][0] = pygame.Vector2(2, 0)
I_OFFSET_DATA[2][1] = pygame.Vector2(0, 0)
I_OFFSET_DATA[2][2] = pygame.Vector2(-2, 1)
I_OFFSET_DATA[2][3] = pygame.Vector2(0, 1)

I_OFFSET_DATA[3][0] = pygame.Vector2(-1, 0)
I_OFFSET_DATA[3][1] = pygame.Vector2(0, 1)
I_OFFSET_DATA[3][2] = pygame.Vector2(1, 0)
I_OFFSET_DATA[3][3] = pygame.Vector2(0, -1)

I_OFFSET_DATA[4][0] = pygame.Vector2(2, 0)
I_OFFSET_DATA[4][1] = pygame.Vector2(0, -2)
I_OFFSET_DATA[4][2] = pygame.Vector2(-2, 0)
I_OFFSET_DATA[4][3] = pygame.Vector2(0, 2)

# O offset data
O_OFFSET_DATA = [[pygame.Vector2() for x in range(4)]]
O_OFFSET_DATA[0][0] = pygame.Vector2(0, 0)
O_OFFSET_DATA[0][1] = pygame.Vector2(0, -1)
O_OFFSET_DATA[0][2] = pygame.Vector2(-1, -1)
O_OFFSET_DATA[0][3] = pygame.Vector2(-1, 0)


class Container:
    def __init__(self, width, height, color, rect_atr, position):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        if rect_atr == 'center':
            self.rect = self.surface.get_rect(center=position)
        elif rect_atr == 'topleft':
            self.rect = self.surface.get_rect(topleft=position)
        elif rect_atr == 'topright':
            self.rect = self.surface.get_rect(topright=position)
        elif rect_atr == 'bottomright':
            self.rect = self.surface.get_rect(bottomright=position)
        elif rect_atr == 'bottomleft':
            self.rect = self.surface.get_rect(bottomleft=position)
        self.display_surface = pygame.display.get_surface()

    def run(self):
        pass
