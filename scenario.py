import pygame as pg
class Scenario:
    def __init__(self, screen, base_path_files,speed_x):
        self.screen = screen
        self.base_path_files = base_path_files
        self.speed_x = speed_x
        self.ground_y=400
        self.background=None
        self.ground=None
        self.grounds_rect=[]
        self.create()

    def create(self):
        self.create_images()
        self.create_rects()
    def create_images(self):
        self.background =  pg.image.load(
            f"{self.base_path_files}assets/sprites/background-day.png").convert()
        self.ground=pg.image.load(f"{self.base_path_files}assets/sprites/base.png").convert()


    def create_rects(self):
        self.grounds_rect=[ self.ground.get_rect(topleft=(self.ground.get_width()*i,self.ground_y)) for i in range(2)]

    def update_position_x(self, dt):
        self.grounds_rect[0].x -= self.speed_x * dt
        self.grounds_rect[1].x -= self.speed_x * dt
        if self.grounds_rect[0].right<0:
            self.grounds_rect[0].x=self.grounds_rect[1].right
        if self.grounds_rect[1].right<0:
            self.grounds_rect[1].x=self.grounds_rect[0].right

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        [self.screen.blit(self.ground,bg) for bg in self.grounds_rect]


    def update(self, dt):
        self.update_position_x(dt)



