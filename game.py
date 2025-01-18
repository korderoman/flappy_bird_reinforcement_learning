import pygame as pg
import sys, time

from bird import Bird
from pipe import Pipe
from scenario import Scenario
from score import Score


class Game:
    def __init__(self, show_game=False):
        self.show_game = show_game
        self.screen = pg.display.set_mode((288, 512))
        self.base_path_files=""
        self.fps=60
        self.clock=pg.time.Clock()
        self.speed_x=200
        self.scenario = Scenario(self.screen,self.base_path_files, self.speed_x)
        self.bird=Bird(self.screen,self.base_path_files)
        self.pipe=Pipe(self.screen,self.base_path_files,self.speed_x)
        self.score=Score(self.screen,self.base_path_files)
        self.score_point=0
        self.is_game_over=False
        self.game_loop()

    def check_event_quit(self):
        pg.quit()
        sys.exit()

    def draw(self):
        self.scenario.draw()
        self.bird.draw()
        self.pipe.draw()
        self.score.draw()

    def update(self,dt):
        if not self.is_game_over:
            self.scenario.update(dt)
            self.bird.update(dt)
            self.pipe.update(dt)
            self.score.update(self.score_point)

    def check_events(self,dt):
        self.check_score(dt)
        self.check_event_collisions()
        self.check_event_keyboard()


    def check_event_keyboard(self):
        for event in pg.event.get():
            # Se configura el evento de salida
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.check_event_quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.bird.flap_by_keyboard()

    def check_event_collisions(self):
        bird_collision_pipe=self.check_bird_collision_with_pipe()
        bird_collision_ground=self.check_bird_collision_with_ground()
        if bird_collision_pipe or bird_collision_ground:
            self.is_game_over=True


    def check_bird_collision_with_ground(self):
        for ground in self.scenario.grounds_rect:
            if self.bird.bird_rect.colliderect(ground):
                return True
            else:
                return False
        return False

    def check_bird_collision_with_pipe(self):
        if len(self.pipe.pipes)>0:
            if self.bird.bird_rect.colliderect(self.pipe.pipes[0]['down']):
                return True
            if self.bird.bird_rect.colliderect(self.pipe.pipes[0]['up']):
                return True

    def check_score(self, dt):
        if not self.is_game_over:
            #Puntaje por cada momento en que esté vivo
            self.score_point=round(self.score_point+0.1,1)
            #Puntaje por cada pipe que haya sido superado
            self.check_score_pipe()
            self.check_score_top()

    def check_score_pipe(self):
        """
        Obtiene el puntaje cuando pasa a través de un pipe
        :return:
        """
        if len(self.pipe.pipes)>0:
            pipe_down=self.pipe.pipes[0]['down']
            if pipe_down.right < self.bird.bird_rect.left < pipe_down.right+4:
               self.score_point=self.score_point+1

    def check_score_top(self):
        if self.bird.bird_rect.midtop[1] <=0:
            self.score_point=round(self.score_point-0.5,1)

    def game_loop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt=new_time-last_time
            last_time = new_time

            self.check_events(dt)
            if self.show_game:
                self.draw()
                self.update(dt)
                pg.display.update()
                self.clock.tick(self.fps)


pg.init()
game=Game(show_game=True)
