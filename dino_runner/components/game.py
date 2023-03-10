import pygame

from dino_runner.utils.constants import (
    BG,
    BG_NIGHT,
    ICON,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    FPS,
    FONT_ARIAL,
    GAME_OVER,
    RESET
    )
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.heart_manager import HeartManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False

        self.game_speed = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur() #dinosaurio
        self.obstacle_manager = ObstacleManager()
        self.heart_manager = HeartManager()
        self.power_up_manager = PowerUpManager()
        self.points = 0

        #
        self.background = BG

        self.home = True
        self.lose = False
        self.night = 1

        self.score = '0000'
        self.high_score = '0000'

    def increase_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        #
        score = int(self.points)
        if self.points < 10:
            self.score = "000" + str(score)
        elif self.points / 10 < 10:
            self.score = "00" + str(score)
        elif self.points / 100 < 10:
            self.score = "0" + str(score)
        else: self.score = str(score)
        
        self.player.check_invincibility()
    
    def run(self):
        # Game loop: events - update - draw
        while self.home or self.playing or self.lose:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                #
                self.home = False
                self.lose = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self.status())

        if self.game_speed > 0 and self.game_speed < 20:
            self.game_speed += 0.8

        if self.playing:
            self.obstacle_manager.update(self.game_speed, self)
            self.power_up_manager.update(self.points, self.game_speed, self.player)
            self.increase_score()
        elif self.lose:
            if user_input[pygame.K_UP] or user_input[pygame.K_SPACE]:
                self.reset()
                self.obstacle_manager.remove()
                self.power_up_manager.remove()
                self.playing = True
                self.lose = False
        else:
            if user_input[pygame.K_UP] or user_input[pygame.K_SPACE]:
                self.home = False
                self.playing = True
                self.game_speed = 1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        if self.playing:
            self.draw_background()
            self.player.draw(self.screen)
            self.obstacle_manager.draw(self.screen)
            self.draw_score()
            self.power_up_manager.draw(self.screen)
            self.heart_manager.draw(self.screen)
        elif self.lose:
            self.draw_background()
            self.obstacle_manager.draw(self.screen)
            self.player.draw(self.screen)
            self.draw_score()
            self.draw_game_over()
        else:
            self.player.draw(self.screen)
            self.draw_home()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width1 = BG_NIGHT.get_width()
        image_width = BG.get_width()
        #self.screen.blit(BG_NIGHT, (self.x_pos_bg, 0))
        #self.screen.blit(BG_NIGHT, (image_width1 + self.x_pos_bg, + 0))

        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            #self.screen.blit(BG_NIGHT, (image_width1 + self.x_pos_bg, + 0))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def draw_score(self):
        font = pygame.font.Font(FONT_ARIAL, 30)
        surface = font.render('HI  '+ self.high_score + '  ' + self.score, True, (0, 0, 0))
        rect = surface.get_rect()
        rect.x = 900
        rect.y = 10
        self.screen.blit(surface, rect)

    def draw_home(self):
        font = pygame.font.Font(FONT_ARIAL, 30)
        surface = font.render("Press the spacebar to play", True, (100, 100, 100))
        rect = surface.get_rect()
        rect.x = 400
        rect.y = 250
        self.screen.blit(surface, rect)

    def draw_game_over(self):
        image1 = GAME_OVER
        image2 = RESET
        rect1 = image1.get_rect()
        rect1.x = 375
        rect1.y = 200
        rect2 = image1.get_rect()
        rect2.x = 515
        rect2.y = 270
        self.screen.blit(image1, rect1)
        self.screen.blit(image2, rect2)

    def reset(self):
        self.heart_manager.reset_lives()
        self.high_score = self.score
        self.points = 0
        self.game_speed = 1
        
    
    def status(self):
        if self.playing:
            return 'playing'
        elif self.lose:
            return 'lose'
        else:
            return 'home'
        
