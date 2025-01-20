import time

from game import Game


class EnvironmentFlappy:
    def __init__(self, show_game, pure_game, flap_velocity=250):
        """
        Crear el entorno para el uso de flappy bird
        :param show_game: Indica si se debe renderizar el juego
        :param pure_game: Indica si es que solo se desea jugar el juego; sin entrenamiento
        :param flap_velocity: Indica la velocidad de flap; cuando es pure_game = True, flap_velocity debe ser
        igual a 250
        """
        self.env=Game(show_game, pure_game, flap_velocity)
        self.width=self.env.width
        self.height=self.env.height
        self.last_time=time.time()


    def restart(self):
        self.env.restart_game()
    def step(self, action):
        new_time = time.time()
        dt = new_time - self.last_time
        self.last_time = new_time
        self.env.game_loop_no_pure_game(dt,action)

