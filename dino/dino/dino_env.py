import gym
from gym import spaces
import numpy as np
import pygame
import os

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GROUND_HEIGHT = 550
GRAVITY = 2
FPS = 60
JUMP_COOLDOWN = 20

class DinoEnv(gym.Env):
    def __init__(self):
        super(DinoEnv, self).__init__()
        self.action_space = spaces.Discrete(2)
        # Updated to include velocity and cooldown in observation space
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, -30, 0, 0]), high=np.array([SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 30, SCREEN_WIDTH, JUMP_COOLDOWN]), dtype=np.float32)

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dino")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dino_image = pygame.image.load(os.path.join(current_dir, 'assets/dino.png'))
        self.tree_image = pygame.image.load(os.path.join(current_dir, 'assets/tree.png'))

        self.dino_width, self.dino_height = self.dino_image.get_size()
        self.tree_width, self.tree_height = self.tree_image.get_size()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.reset()

    def reset(self):
        self.dino = pygame.Rect(100, GROUND_HEIGHT - self.dino_height, self.dino_width, self.dino_height)
        self.dino_vel_y = 0
        self.is_jumping = False
        self.jump_cooldown = 0
        self.trees = [pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - self.tree_height, self.tree_width, self.tree_height)]
        self.score = 0
        self.game_over = False
        return self._get_obs()

    def step(self, action):
        reward = 0.1  # Base survival reward

        closest_tree = self.trees[0]
        distance_to_next_tree = closest_tree.x - self.dino.x

        if action == 1 and not self.is_jumping and self.jump_cooldown == 0:
            if distance_to_next_tree > 300:
                reward -= 5
            else:
                reward += 10
            self.dino_vel_y = -30
            self.is_jumping = True
            self.jump_cooldown = JUMP_COOLDOWN

        if not self.game_over:
            if self.is_jumping:
                self.dino.y += self.dino_vel_y
                self.dino_vel_y += GRAVITY
                if self.dino.bottom > GROUND_HEIGHT:
                    self.dino.bottom = GROUND_HEIGHT
                    self.is_jumping = False
                    self.dino_vel_y = 0

            for tree in self.trees:
                tree.x -= 10
                if tree.x < -self.tree_width:
                    self.trees.remove(tree)
                    self.trees.append(pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - self.tree_height, self.tree_width, self.tree_height))
                    self.score += 10
                    reward += 10

            for tree in self.trees:
                if self.dino.colliderect(tree):
                    self.game_over = True
                    reward = -100

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        terminated = self.game_over
        truncated = False
        info = {}
        return self._get_obs(), reward, terminated, info

    def _get_obs(self):
        closest_tree = self.trees[0]
        distance_to_next_tree = closest_tree.x - self.dino.x
        return np.array([self.dino.y, closest_tree.x, closest_tree.y, self.dino_vel_y, distance_to_next_tree, self.jump_cooldown], dtype=np.float32)


    def render(self, mode='human'):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.dino_image, self.dino)
        for tree in self.trees:
            self.screen.blit(self.tree_image, tree)

        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text_game_over = self.font.render(f'Game Over! Final Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(text_game_over, (SCREEN_WIDTH // 2 - text_game_over.get_width() // 2, SCREEN_HEIGHT // 2))
            text_restart = self.font.render('Press R to Restart', True, (255, 0, 0))
            self.screen.blit(text_restart, (SCREEN_WIDTH // 2 - text_restart.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        self.clock.tick(FPS)

    def close(self):
        pygame.quit()

# Register the environment
gym.envs.registration.register(
    id='Dino-v0',
    entry_point='dino_env:DinoEnv',
)
