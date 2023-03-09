import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.image = image
        self.type = 0
        self.step_index = 0
        
        super().__init__(image, self.type)
        self.rect.y = 325 - (random.randint(80, 270))
        
    def update(self, game_speed, obstacles):

        self.rect.x -= game_speed

        if self.rect.x < -100:
            obstacles.pop()

        if self.step_index >= 10:
            self.step_index = 0
        
        self.fly()

    def fly(self):
        if self.step_index < 5:
            self.type = 0
        else:
            self.type = 1

        self.step_index += 1
        

        