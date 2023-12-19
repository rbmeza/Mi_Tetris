from settings import *
from random import choice, randint
from timer import Timer


class Game(Container):
    def __init__(self):
        super().__init__(GAME_WIDTH, GAME_HEIGHT, BLACK,
                         "center", (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.sprites = pygame.sprite.Group()
        self.bag = list(TETROMINOS.keys())

        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(100)

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.create_new_tetromino()
        # self.tetromino = Tetromino(
        #     self.sprites,
        #     "I",
        #     self.create_new_tetromino,
        #     self.field_data)

        # timer
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME),
        }
        self.timers['vertical move'].activate()
        self.pause = False

    def create_new_tetromino(self):
        self.check_finished_rows()
        shape = self.bag.pop(randint(0, len(self.bag) - 1))
        print(shape)
        self.tetromino = Tetromino(
            self.sprites,
            shape,
            self.create_new_tetromino,
            self.field_data)

        if not self.bag:
            self.bag = list(TETROMINOS.keys())

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR,
                             (x, 0), (x, self.surface.get_height()))
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y),
                             (self.surface.get_width(), y))

    def input(self):
        keys = pygame.key.get_pressed()
        if self.pause:
            if keys[pygame.K_p]:
                self.pause = False
                self.timers['vertical move'].activate()
            return
        # move left
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()

            # move right
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()
                pass

            # move down
            if keys[pygame.K_DOWN]:
                pass
        if not self.timers['rotate'].active:
            # rotate clockwise
            if keys[pygame.K_UP]:
                self.tetromino.rotate(1, True)
                self.timers['rotate'].activate()

            # rotate counterclockwise
            if keys[pygame.K_z]:
                self.tetromino.rotate(-1, True)
                self.timers['rotate'].activate()

        # pause game
        if keys[pygame.K_p]:
            self.timers['vertical move'].deactivate()
            self.pause = True

    def check_finished_rows(self):
        # get the full rows indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:

                # delete the blocks
                for block in self.field_data[delete_row]:
                    block.kill()

                # move the rows down
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            # rebuild the field data
            self.field_data = [
                [0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            for row in self.field_data:
                print(row)

    def run(self):
        # update
        self.input()
        if not self.pause:
            self.timer_update()
            self.sprites.update()

        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(
            self.surface, self.rect)

        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)


class Tetromino:
    def __init__(self, group, shape, create_new_tetromino, field_data):
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        self.rotation_index = 0

        self.blocks = [Block(group, self.color, pos)
                       for pos in self.block_positions]

    # collisions
    def next_rotation_collide(self, blocks, pos_after_offset):
        for block in blocks:
            if block.rotation_collide(self.field_data, pos_after_offset[blocks.index(block)]):
                return True

    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(
            int(block.pos.x + amount), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks):
        collision_list = [block.vertical_collide(
            int(block.pos.y + 1), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    # movement
    def move_down(self):
        if self.next_move_vertical_collide(self.blocks):
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()
            return
        for block in self.blocks:
            block.pos.y += 1
            block.rect.y += CELL_SIZE

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount
                block.rect.x += amount * CELL_SIZE

    def rotate(self, direction: int, should_offset):
        if self.shape == 'O':
            return
        old_rotation_index = self.rotation_index
        self.rotation_index += direction
        self.rotation_index = mod(self.rotation_index, 4)

        # pivot point
        pivot = self.blocks[0].pos

        # new block positions on the field after rotate
        new_block_positions = [block.rotate(
            pivot, direction) for block in self.blocks]

        # check if the rotation is possible
        if should_offset:
            # we are checking for a valid rotation
            can_offset = self.check_offset(
                old_rotation_index, new_block_positions)

            if not can_offset:
                self.rotate(-direction, False)
                return

    def check_offset(self, old_rotation_index: int, new_block_positions: list()):
        # offset data
        if self.shape == 'I':
            offset_data = I_OFFSET_DATA
        elif self.shape == 'O':
            offset_data = O_OFFSET_DATA
        else:
            offset_data = JLSTZ_OFFSET_DATA

        # get the offset vectors
        endoffset = pygame.Vector2(0, 0)
        move_possible = False

        for test_index in range(5):
            offsetval1 = offset_data[test_index][old_rotation_index]
            offsetval2 = offset_data[test_index][self.rotation_index]
            endoffset = offsetval1 - offsetval2

            pos_after_offset = [pos + endoffset for pos in new_block_positions]
            # test if the offset is possible
            if not self.next_rotation_collide(self.blocks, pos_after_offset):
                move_possible = True
                break

        if move_possible:
            for block in self.blocks:
                block.pos = pos_after_offset[self.blocks.index(block)]

            return True


class Block(pygame.sprite.Sprite):
    def __init__(self, group, color, pos):
        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def rotate(self, pivot: pygame.Vector2, direction: int):
        distance = self.pos - pivot
        rotated = distance.rotate(direction * 90)
        new_pos = rotated + pivot
        return new_pos

    def rotation_collide(self, field_data, new_pos):
        x = int(new_pos.x)
        y = int(new_pos.y)
        if not 0 <= x < COLUMNS:
            return True
        if y >= ROWS:
            return True
        if field_data[y][x]:
            return True

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True
        if field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE


def mod(x, m):
    result = (x % m + m) % m
    return result
