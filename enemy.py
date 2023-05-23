import random, os, pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Enemy:
    def __init__(self) -> None:
        self.speed = random.random() + 1

        self.stun_time = (self.speed + 1) * 1000

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.alive = True

        self.font = pygame.font.Font(os.path.join('apple.ttf'), 16)
        self.text = self.font.render("#", True, self.color)
        self.stun_text = self.font.render("x", True, self.color)

        self.pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.stun_pos = (0, 0)
        
        self.stun_start = 0

    def set_alive(self, state: bool) -> None:
        self.alive = state

    def set_stun_pos(self, x: int, y: int) -> None:
        self.stun_pos = (x, y)

    def set_stun_start(self, time: int) -> None:
        self.stun_start = time