# Complete your game here
import pygame
from random import randint

class Camel:
    def __init__(self):
        # initiate pygame
        pygame.init()

        # constants:
        self.WIDTH = 24
        self.HEIGHT = 6
        self.TICK = 8
        self.MAX_MOVES = 50
        self.MIN_COINS = 5

        # load all sprites and start new game
        self.load_images()
        self.new_game()
        
        # set up caption, screen and clock
        pygame.display.set_caption("0ld Camel's Game")
        self.scale_x, self.scale_y = self.get_scales()
        window_h = self.scale_y * self.HEIGHT
        window_w = self.scale_x * self.WIDTH
        self.window = pygame.display.set_mode((window_w, window_h + self.scale_y))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.main_loop()

    def get_coins(self):
        self.coin_x = randint(0, self.WIDTH - 1)
        self.coin_y = randint(0, self.HEIGHT - 1)
        return(self.coin_x, self.coin_y)
            
    def load_images(self):
        self.images = {}
        for name in ["coin", "door", "monster", "robot"]:
            self.images[name] = pygame.image.load(name + ".png")
    
    def new_game(self):
        self.map = [[1 for i in range(self.WIDTH)] for j in range(self.HEIGHT)]
        self.scale_x, self.scale_y = self.get_scales()
        self.robot_x, self.robot_y = 0, (self.HEIGHT - 1) * self.scale_y
        self.score = 0
        self.moves = 0
        self.speed = 0.25
        self.monster_x1, self.monster_y1 = self.WIDTH / 2, 0
        self.coins = []

    def get_scales(self): 
        # get the max height and width of coin, monster, door and robot are 
        scale_x, scale_y = 0, 0
        for value in self.images.values():
            scale_x = max(scale_x, value.get_width())
            scale_y = max(scale_y, value.get_height())
        return scale_x, scale_y

    def draw_background(self):
        # draw green back ground with gray borders
        for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    back = pygame.Rect(x * self.scale_x, y * self.scale_y, self.scale_x, self.scale_y)
                    pygame.draw.rect(self.window, "green", back, width=0)
                    pygame.draw.rect(self.window, "gray", back, width=1)

    def collect_coins(self):
        # place 5 coins at random positions
        if len(self.coins) < 5:
            self.coins.append(self.get_coins())
        # check for collision between robot and coin, if so, coin is collected and new coin place at random.
        for self.coin_x, self.coin_y in self.coins:
            coin_w, coin_h = self.images["coin"].get_width(), self.images["coin"].get_height()
            self.window.blit(self.images["coin"], (self.scale_x * (self.coin_x + 1 / 2) - coin_w / 2, self.coin_y * self.scale_y + self.scale_y / 2 - coin_h / 2))
            coin_rect = pygame.Rect(self.coin_x * self.scale_x, self.coin_y * self.scale_y, self.images["coin"].get_width(), self.images["coin"].get_height())
            if coin_rect.colliderect(self.robot_rect):
                self.score += 1
                self.coins.remove((self.coin_x, self.coin_y))

    def monsters_move(self):
        # make monster patrolling between top and bottom rows
        if self.speed > 0 and self.monster_y1 > self.HEIGHT - 1 or self.monster_y1 < 0 and self.speed < 0:
            self.speed = -self.speed
        self.monster_y1 += self.speed
        # check for collision with robot
        monster_rect = pygame.Rect(self.monster_x1 * self.scale_x, self.monster_y1 * self.scale_y, self.images["monster"].get_width(), self.images["monster"].get_height())
        if monster_rect.colliderect(self.robot_rect):
            self.speed = 0
            return True
        return False
        
    def draw_window(self):
        self.window.fill((0, 0, 0))
        self.draw_background()
        
        self.robot_rect = pygame.Rect(self.robot_x, self.robot_y, self.images["robot"].get_width(), self.images["robot"].get_height())
        self.window.blit(self.images["door"], ((self.WIDTH - 0.5) * self.scale_x - self.images["door"].get_width()/2, self.scale_y / 2 - self.images["door"].get_height() / 2))
        self.window.blit(self.images["robot"], (self.robot_x, self.robot_y))
        self.window.blit(self.images["monster"], (self.monster_x1 * self.scale_x, self.monster_y1 * self.scale_y))
        self.collect_coins()
        self.monsters_move()
        self.draw_text()
        pygame.display.flip()

    def draw_text(self):
        color = "green" if self.moves <= 30 else "red"
        game_text = self.game_font.render("Moves: " + str(self.moves), True, color)
        self.window.blit(game_text, (25, self.HEIGHT * self.scale_y + 15))

        color = "green" if self.score >= 5 else "red"
        game_text = self.game_font.render("Coins collected: " + str(self.score), True, color)
        self.window.blit(game_text, (25, self.HEIGHT * self.scale_y + 45))

        game_text = self.game_font.render("F2 = new game, Esc = exit game", True, color)
        self.window.blit(game_text, (300, self.HEIGHT * self.scale_y + 45))

        if self.game_solved():
            game_text = self.game_font.render("Congratulations! You win", True, color)
            self.window.blit(game_text, (300, self.HEIGHT * self.scale_y + 15))

            game_text = self.game_font.render("F2 = new game, Esc = exit game", True, color)
            self.window.blit(game_text, (300, self.HEIGHT * self.scale_y + 45))

        if self.monsters_move() or self.moves >= self.MAX_MOVES:
            game_text = self.game_font.render("Sorry! You lost", True, "red")
            self.window.blit(game_text, (300, self.HEIGHT * self.scale_y + 15))

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            if self.game_solved() or self.monsters_move() or self.moves >= self.MAX_MOVES:
                self.speed = 0 # stop monster
                self.draw_text()
            self.clock.tick(self.TICK)
        

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
        # not more than 50 moves
        if self.moves >= self.MAX_MOVES: 
            return True

        if self.game_solved():
            return
        
        if self.monsters_move():
            return

        if self.robot_y + move_y * self.scale_y >= (len(self.map)) * self.scale_y or self.robot_y + move_y * self.scale_y < 0:
            return
        if self.robot_x + move_x * self.scale_x >= (len(self.map[0])) * self.scale_x or self.robot_x + move_x * self.scale_x < 0:
            return
        self.robot_y += move_y * self.scale_y
        self.robot_x += move_x * self.scale_x
        self.moves += 1
        
    def game_solved(self):
        if self.robot_x == (self.WIDTH - 1) * self.scale_x and self.robot_y == 0 and self.score >= self.MIN_COINS:
            return True

if __name__ == "__main__":
    Camel()
