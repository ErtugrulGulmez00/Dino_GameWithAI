import os
import gym
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.utils import get_device
from dino_env import DinoEnv
import warnings

warnings.filterwarnings("ignore")

# Create and wrap the environment
env = gym.make('Dino-v0')

# Check if GPU is available and set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")



# Define the model with tuned hyperparameters
model = PPO(
    'MlpPolicy',
    env,
    verbose=0,
    device=device,
    learning_rate=3e-4,
    n_steps=4096,
    batch_size=4096,
    n_epochs=50,
    gamma=0.9999999

)


# Train the model
model.learn(total_timesteps=400000)

# Save the model
model.save('dino_model')

# Close the environment
env.close()