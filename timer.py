from pygame.time import get_ticks


class Timer:
    def __init__(self, duration, repeated=False, function=None):
        self.duration = duration
        self.repeated = repeated
        self.function = function

        self.start_time = 0
        self.active = False

    def activate(self):
        self.start_time = get_ticks()
        self.active = True

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration and self.active:

            # call a function
            if self.function:
                self.function()

            # reset timer
            self.deactivate()

            # repeat the timer
            if self.repeated:
                self.activate()
