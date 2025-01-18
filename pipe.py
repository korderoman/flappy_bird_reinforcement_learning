from random import randint

import pygame as pg

class Pipe:
    def __init__(self,screen, base_path_files, speed_x):
        self.screen = screen
        self.base_path_files = base_path_files
        self.speed_x = speed_x
        self.pipe_up=None
        self.pipe_down=None
        self.pipe_up_rect=None
        self.pipe_down_rect=None
        self.pipe_gap=100
        self.width, self.height = self.screen.get_size()
        self.base_y_position_pipe_up_rect=100
        self.pipes=[]
        self.time_pipe=70
        self.create()

    def create(self):
        self.create_pipe_img()

    def create_pipe_img(self):
        pipe_asset_path = f"{self.base_path_files}assets/sprites/pipe-green.png"
        self.pipe_up = pg.transform.rotate(pg.image.load(pipe_asset_path).convert_alpha(), 180)
        self.pipe_down = pg.image.load(pipe_asset_path).convert_alpha()

    def create_pipe_rects(self):
        position_x=self.width+150
        position_y_up=randint(self.base_y_position_pipe_up_rect,self.height/2)
        position_y_down=position_y_up +self.pipe_gap
        pipe_up_rect = self.pipe_up.get_rect(midbottom=(position_x, position_y_up))
        pipe_down_rect = self.pipe_down.get_rect(midtop=(position_x, position_y_down))
        pipe={
            "up":pipe_up_rect,
            "down":pipe_down_rect,
        }
        self.pipes.append(pipe)

    def draw(self):
        [self.draw_pipes(pipe) for pipe in self.pipes]

    def draw_pipes(self, pipe):
        self.screen.blit(self.pipe_up, pipe['up'])
        self.screen.blit(self.pipe_down, pipe['down'])

    def update(self,dt):
        self.update_pipe_rects(dt)
        self.update_add_pipe(dt)
        self.update_delete_pipe(dt )
        #print(len(self.pipes))

    def update_pipe_rect(self,dt, pipe):
        pipe['up'].x -= self.speed_x * dt
        pipe['down'].x -= self.speed_x * dt

    def update_pipe_rects(self,dt):
        [self.update_pipe_rect(dt, pipe) for pipe in self.pipes]

    def update_add_pipe(self,dt):
        if self.time_pipe>70:
            self.create_pipe_rects()
            self.time_pipe=0
        self.time_pipe += 1
    def update_delete_pipe(self,dt):
        if len(self.pipes)>0:
            if self.pipes[0]['up'].right<-self.pipe_up.get_width():
                self.pipes.pop(0)

