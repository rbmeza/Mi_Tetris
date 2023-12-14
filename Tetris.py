from settings import *

# components
from game import Game
from score import Score
from preview import Preview
from hold import Hold


class Main():

    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Best Tetris Chileno")

        # components
        self.game = Game()
        self.score = Score()
        self.preview = Preview()
        self.hold = Hold()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # display
            self.display_surface.fill(GRAY)

            # components
            self.game.run()
            self.score.run()
            self.preview.run()
            self.hold.run()

            # updating the game
            pygame.display.update()
            self.clock.tick(60)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main = Main()
    main.run()
