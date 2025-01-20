from numpy.random import randint

from environment_flappy import EnvironmentFlappy
import numpy as np

env= EnvironmentFlappy(show_game=True, pure_game=False, flap_velocity=32)
env.restart()

SCREEN_WIDTH = env.width
SCREEN_HEIGHT = env.height

STATE_SPACE={
    "bird_y":np.linspace(0,SCREEN_HEIGHT,20),
    "pipe_x":np.linspace(0,SCREEN_WIDTH,10),
    "pipe_gap_y":np.linspace(0,SCREEN_HEIGHT,10),
    "velocity":np.linspace(-15,15,10)
}

while True:
    action=np.random.choice([0, 1], p=[0.7, 0.3])
    env.step(action)