import pygame


class Card:
    def __init__(self):
        pygame.init()

        # self.images = self.load_images()
        self.load_images()
        self.new_game()
        self.width, self.height = self.get_size()
        self.x_scale, self.y_scale = self.get_scales() # 50, 86

        window_height = self.y_scale * self.height
        window_width = self.x_scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height))

        self.main_loop()

    def get_size(self):
        return 6, 4

    def new_game(self):
        self.width, self.height = self.get_size()
        self.map = [
            [1 for i in range(self.width)] for j in range(self.height)
        ]
        return self.map

    def load_images(self):
        self.images = []
        for name in ["coin", "door", "monster", "robot"]:
            self.images.append(pygame.image.load(name + ".png"))
        return self.images

    def get_scales(self):
        self.images = self.load_images()
        x_scale = max([self.images[i].get_width() for i in range(4)])
        y_scale = max([self.images[i].get_height() for i in range(4)])
        return x_scale, y_scale

    def draw_window(self):
        self.window.fill((0, 0, 0))
        images = self.images
        k = 0
        for y in range(self.height):
            for x in range(self.width):
                back = pygame.Rect(x * self.x_scale, y * self.y_scale, self.x_scale, self.y_scale)
                pygame.draw.rect(self.window, "green", back, width=0)
                pygame.draw.rect(self.window, "red", back, width=1)

                self.window.blit(images[k % 4], (x * self.x_scale + self.x_scale / 2 - images[k % 4].get_width() / 2, y * self.y_scale + self.y_scale / 2 - images[k % 4].get_height() / 2))
                pygame.draw.circle(self.window, "red", (x * self.x_scale + self.x_scale / 2, y * self.y_scale + self.y_scale / 2), 15, 2)
                k += 1
        
        pygame.display.flip()


    def main_loop(self):
        while True:
            self.draw_window()
            self.check_event()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    print("mouse clicked at", x, y)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

cau = Card()
print(cau.x_scale, cau.y_scale)