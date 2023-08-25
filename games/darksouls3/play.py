import gymnasium
import soulsgym
import pyautogui
import logging
from collections import defaultdict
import numpy as np
from tqdm import tqdm
import matplotlib as plt
from soulsgym.games import DarkSoulsIII
from stable_baselines3 import DQN
import os




def playDarkSouls3(model):
    #Necessary to start

    game = DarkSoulsIII()
    game.game_speed = 3
    pyautogui.press("alt")
    

    model.learn(total_timesteps=500, reset_num_timesteps=False, tb_log_name="DQN")

if __name__ == "__main__":
    # models_dir = "models/DQN"
    # logdir = "logs"

    # if not os.path.exists(models_dir):
    #     os.makedirs(models_dir)

    env = gymnasium.make("SoulsGymIudex-v0")
    model = DQN("MultiInputPolicy", env, verbose = 1)
    playDarkSouls3(model)
    env.close()
   
    