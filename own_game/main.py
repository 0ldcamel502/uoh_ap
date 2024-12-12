# Complete your game here
import pygame
from random import randint

# TO DO:
# 1. Score
# 2. game solve = True when Robot get to Door
# 3. Add Monster
# 4. Make Monster patrolling
# 5. Robot dies if collies with Monster

class Camel:
    def __init__(self):
        # initiate pygame
        pygame.init()

        # constants:
        self.WIDTH = 24
        self.HEIGHT = 6

        self.load_images()
        self.new_game()
        self.scale_x, self.scale_y = self.get_scales()
        
        window_h = self.scale_y * self.HEIGHT
        window_w = self.scale_x * self.WIDTH
        self.window = pygame.display.set_mode((window_w, window_h + self.scale_y))

        self.robot_x, self.robot_y = 0, (len(self.map) - 1) * self.scale_y
        self.coins = []

        pygame.display.set_caption("0ld Camel's Game")
        self.clock = pygame.time.Clock()
        self.main_loop()

    def get_coins(self):
        self.coin_x = randint(0, len(self.map[0]) - 1)
        self.coin_y = randint(0, len(self.map) - 1)
        return(self.coin_x, self.coin_y)
            

    def load_images(self):
        self.images = {}
        for name in ["coin", "door", "monster", "robot"]:
            self.images[name] = pygame.image.load(name + ".png")
    
    def new_game(self):
        self.map = [[1 for i in range(self.WIDTH)] for j in range(self.HEIGHT)]
        self.scale_x, self.scale_y = self.get_scales()
        self.robot_x, self.robot_y = 0, (len(self.map) - 1) * self.scale_y

    def get_scales(self):
        scale_x, scale_y = 0, 0
        for key, value in self.images.items():
            scale_x = max(scale_x, value.get_width())
            scale_y = max(scale_y, value.get_height())
        return scale_x, scale_y

    def draw_window(self):
        self.window.fill((0, 0, 0))
        if len(self.coins) < 5:
            self.coins.append(self.get_coins())

        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                back = pygame.Rect(x * self.scale_x, y * self.scale_y, self.scale_x, self.scale_y)
                pygame.draw.rect(self.window, "green", back, width=0)
                pygame.draw.rect(self.window, "gray", back, width=1)
        robot_rect = pygame.Rect(self.robot_x, self.robot_y, self.images["robot"].get_width(), self.images["robot"].get_height())
        print("robot rect",robot_rect)
        for coin in self.coins:
            coin_x, coin_y = coin
            coin_image = self.images["coin"]
            self.window.blit(coin_image, (coin_x * self.scale_x + self.scale_x / 2 - coin_image.get_width() / 2, coin_y * self.scale_y + self.scale_y / 2 - coin_image.get_height() / 2))
            
            coin_rect = pygame.Rect(coin_x * self.scale_x, coin_y * self.scale_y, self.images["coin"].get_width(), self.images["coin"].get_height())
            print("coin rect",coin_rect)
            if coin_rect.colliderect(robot_rect):
                print("collide")
                self.coins.remove(coin)
        self.window.blit(self.images["door"], ((len(self.map[0]) - 0.5) * self.scale_x - self.images["door"].get_width()/2, self.scale_y / 2 - self.images["door"].get_height() / 2))
        
        self.window.blit(self.images["robot"], (self.robot_x, self.robot_y))
        

        pygame.display.flip()

    def main_loop(self):
        while True:
            self.check_events()
            self.get_coins()
            self.draw_window()
            self.clock.tick(1)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()
    def move(self, move_y, move_x):
        if self.game_solved():
            return

        if self.robot_y + move_y * self.scale_y >= (len(self.map)) * self.scale_y or self.robot_y + move_y * self.scale_y < 0:
            return
        if self.robot_x + move_x * self.scale_x >= (len(self.map[0])) * self.scale_x or self.robot_x + move_x * self.scale_x < 0:
            return
        self.robot_y += move_y * self.scale_y
        self.robot_x += move_x * self.scale_x
        print(self.robot_x, self.robot_y, len(self.map[0]) * self.scale_x, len(self.map) * self.scale_y)

    def game_solved(self):
        if self.robot_x == (len(self.map[0]) - 1) * self.scale_x and self.robot_y == (len(self.map) - 1) * self.scale_y:
            return True

cau = Camel()

print(cau.get_coins())