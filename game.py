import pygame as pg
import sys, time
import os

from bird import Bird
from pipe import Pipe
from scenario import Scenario
from score import Score
from restart_game import RestartGame


class Game:
    def __init__(self, show_game=False, pure_game=True, flap_velocity=250):
        """
        Clase que representa el juego de Flappy Bird
        :param show_game: Hace que el juego se muestre
        :param pure_game:  Hace que el juego solo sirva como juego, cuando es false es posible extraer data
        para la medición del entorno
        :param flap_velocity: Velocidad de flap (puede ser afectada para el proceso de aprendizaje)
        """
        self.show_game = show_game
        self.height = 512
        self.width = 288
        self.screen = pg.display.set_mode((self.width, self.height))
        self.base_path_files=os.path.dirname(os.path.abspath(__file__))+"/"
        self.fps=60
        self.clock=pg.time.Clock()
        self.speed_x=200
        self.scenario = Scenario(self.screen,self.base_path_files, self.speed_x)
        self.bird=Bird(self.screen,self.base_path_files, flap_velocity)
        self.pipe=Pipe(self.screen,self.base_path_files,self.speed_x)
        self.score=Score(self.screen,self.base_path_files,self.bird, self.pipe)
        self.restart=RestartGame(self.screen,self.base_path_files)
        self.score_point=0
        self.is_game_over=True
        self.game_loop(pure_game)

    def check_event_quit(self):
        pg.quit()
        sys.exit()




    def check_event_keyboard(self, pure_game):
        for event in pg.event.get():
            # Se configura el evento de salida
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.check_event_quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and pure_game:
                self.bird.flap_by_keyboard()
            if event.type == pg.MOUSEBUTTONUP and self.is_game_over:
                if self.restart.check_if_click_restart(pg.mouse.get_pos()):
                    self.restart_game()

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

    def check_score_still_alive(self):
        # Puntaje por cada momento en que esté vivo
        self.score_point = round(self.score_point + 0.1, 1)

    def check_score(self, dt):
        if not self.is_game_over:
            self.check_score_still_alive()
            #Puntaje por cada pipe que haya sido superado
            self.check_score_pipe()
            #Puntaje por tocar el techo
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
# ---------------------------------------------- MÉTODOS PRINCIPALES DEL JUEGO ------------------------------------
    def restart_game(self):
        self.score_point=0
        self.bird.restart()
        self.pipe.restart()
        self.score.restart()
        self.scenario.restart()
        self.is_game_over=False

    def draw(self):
        self.scenario.draw()
        self.bird.draw()
        self.pipe.draw()
        self.score.draw()
        self.restart.draw(self.is_game_over)
    def flap_by_action(self, action):
        if action==1 and not self.is_game_over:
            self.bird.flap_by_keyboard()

    def update(self, dt):
        if not self.is_game_over:
            self.scenario.update(dt)
            self.bird.update(dt)
            self.pipe.update(dt)
            self.score.update(self.score_point)

    def check_events(self, dt,pure_game):
        self.check_score(dt)
        self.check_event_collisions()
        self.check_event_keyboard(pure_game)

    def restart(self):
        self.bird.restart()
        self.pipe.restart()
        self.score_point=0
        self.is_game_over=False

    def game_loop(self, pure_game):
        if pure_game:
            self.game_loop_pure_game()


    def game_loop_no_pure_game(self,dt,action):
        """
        Utilizado para procesos de entrenamiento
        :param dt: Intervalo de tiempo
        :param action: Acción a realizar (0 o 1)
        :return:
        """
        self.check_events(dt, pure_game=False)

        self.flap_by_action(action)
        if self.show_game:
            self.draw()
            self.update(dt)
            pg.display.update()
            self.clock.tick(self.fps)
        return self.score.check_score_by_step(self.is_game_over)
    def game_loop_pure_game(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            self.check_events(dt, pure_game=True)
            if self.show_game:
                self.draw()
                self.update(dt)
                pg.display.update()
                self.clock.tick(self.fps)



pg.init()
#game=Game(show_game=True)
