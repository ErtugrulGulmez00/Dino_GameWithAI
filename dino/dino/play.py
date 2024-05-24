import pygame

# Initialize Pygame
pygame.init()


# Mixer modülünü başlat
pygame.mixer.init()

# Arka plan müziğini yükle
pygame.mixer.music.load('assets/Neset-Ertas-Gel-Yanima-Gel.mp3')

# Müziği sonsuz döngüde oynat
pygame.mixer.music.play(-1)


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GROUND_HEIGHT = 550
GRAVITY = 2
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Game:
    def __init__(self):
        # Screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dino")

        # Clock
        self.clock = pygame.time.Clock()

        # Load images
        self.dino_image = pygame.image.load('assets/dino.png')
        self.tree_image = pygame.image.load('assets/tree.png')
        self.dino_width, self.dino_height = self.dino_image.get_size()
        self.tree_width, self.tree_height = self.tree_image.get_size()

        # Dinosaur
        self.dino = pygame.Rect(100, GROUND_HEIGHT - self.dino_height, self.dino_width, self.dino_height)
        self.dino_vel_y = 0
        self.is_jumping = False

        # Trees
        self.trees = [pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - self.tree_height, self.tree_width, self.tree_height)]
        self.tree_speed = 10

        # Score
        self.score = 0

        # Game state
        self.game_over = False

        # Font
        self.font = pygame.font.Font(None, 36)

        # Main game loop flag
        self.running = True

    def reset(self):
        self.game_over = False
        self.score = 0
        self.dino.y = GROUND_HEIGHT - self.dino_height
        self.trees = [pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - self.tree_height, self.tree_width, self.tree_height)]
        self.dino_vel_y = 0
        self.is_jumping = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.dino.bottom >= GROUND_HEIGHT and not self.game_over:
                    self.dino_vel_y = -30
                    self.is_jumping = True
                if event.key == pygame.K_r and self.game_over:
                    self.reset()

    def update_game_logic(self):
        if not self.game_over:
            # Dinosaur movement
            if self.is_jumping:
                self.dino.y += self.dino_vel_y
                self.dino_vel_y += GRAVITY
                if self.dino.bottom > GROUND_HEIGHT:
                    self.dino.bottom = GROUND_HEIGHT
                    self.is_jumping = False
                    self.dino_vel_y = 0

            # Trees movement
            for tree in self.trees:
                tree.x -= self.tree_speed
                if tree.x < -self.tree_width:
                    self.trees.remove(tree)
                    self.trees.append(
                        pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - self.tree_height, self.tree_width, self.tree_height))
                    self.score += 10  # Increment score as trees go off screen

            # Collision detection
            for tree in self.trees:
                if self.dino.colliderect(tree):
                    self.game_over = True  # Game over condition

    def draw_elements(self):
        self.screen.fill(WHITE)

        # Draw dinosaur
        self.screen.blit(self.dino_image, self.dino)

        # Draw trees
        for tree in self.trees:
            self.screen.blit(self.tree_image, tree)

        # Display score
        text = self.font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(text, (10, 10))

        # Game Over screen
        if self.game_over:
            text_game_over = self.font.render(f'Game Over! Final Score: {self.score}', True, BLACK)
            self.screen.blit(text_game_over, (SCREEN_WIDTH // 2 - text_game_over.get_width() // 2, SCREEN_HEIGHT // 2))
            text_restart = self.font.render('Press R to Restart', True, RED)
            self.screen.blit(text_restart, (SCREEN_WIDTH // 2 - text_restart.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_logic()
            self.draw_elements()

            # Update the display
            pygame.display.flip()

            # Frame rate
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
