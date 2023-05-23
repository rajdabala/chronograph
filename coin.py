import random, os, pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Coin:
    def __init__(self):
        self.speed = random.randint(1, 5)

        self.color = (212, 175, 55)

        self.collected = False

        self.font = pygame.font.Font(os.path.join('apple.ttf'), 16)
        self.text = self.font.render("$", True, self.color)

        self.pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

        if random.random() < 0.5:
            self.xy = 0
        else:
            self.xy = 1

    def collect(self, state: bool) -> None:
        self.collected = state