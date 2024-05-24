import os
import gym
from stable_baselines3 import PPO
import pygame
from dino_env import DinoEnv

import warnings

warnings.filterwarnings("ignore")


pygame.init()

# Mixer modülünü başlat
pygame.mixer.init()

# Arka plan müziğini yükle
pygame.mixer.music.load('assets/Neset-Ertas-Gel-Yanima-Gel.mp3')

# Müziği sonsuz döngüde oynat
pygame.mixer.music.play(-1)

# Load the environment
env = gym.make('Dino-v0')

# Load the trained model

model = PPO.load("dino_model.zip")

obs = env.reset()
done = False



# Game over handling to display the final score and restart option
while True:
    env.render()
    action, _states = model.predict(obs)
    obs, reward, terminated, info = env.step(action)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.close()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                obs = env.reset()

env.close()
