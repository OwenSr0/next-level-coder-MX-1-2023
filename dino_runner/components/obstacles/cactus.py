import random

from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325
        
    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if str(self.image) == '[<Surface(48x95x32 SW)>, <Surface(99x95x32 SW)>, <Surface(102x95x32 SW)>]' and not self.rect.y == 300:
            self.rect.y = 300
        elif str(self.image) == '[<Surface(40x71x32 SW)>, <Surface(68x71x32 SW)>, <Surface(105x71x32 SW)>]' and not self.rect.y == 325:
            self.rect.y = 325

        if self.rect.x < -100:
            obstacles.pop()