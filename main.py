import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 350, 600
TILESIZE = 32
FLOOR_HEIGHT = TILESIZE * 5
PLAYER_SPEED = 8
APPLE_FALL_SPEED = [3, 4, 5]  # Different speeds for variety
APPLE_SPAWN_Y = -50
APPLE_LIMIT = 3  # Max apples at once

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Assets
floor_image = pygame.image.load('assets/floor.png').convert_alpha()
floor_image = pygame.transform.scale(floor_image, (TILESIZE * 15, FLOOR_HEIGHT))
floor_rect = floor_image.get_rect(bottomleft=(0, SCREEN_HEIGHT))

player_image = pygame.image.load('assets/player_static.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (TILESIZE, TILESIZE * 2))

apple_image = pygame.image.load('assets/apple.png').convert_alpha()
apple_image = pygame.transform.scale(apple_image, (TILESIZE, TILESIZE))

font = pygame.font.Font('assets/PixeloidMono.ttf', TILESIZE // 2)

# Sound FX
pickup = pygame.mixer.Sound('assets/powerup.mp3')
pickup.set_volume(0.1)


class Player:
    """Player controlled by the user."""
    def __init__(self):
        self.image = player_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - FLOOR_HEIGHT - (self.image.get_height() / 2)))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(PLAYER_SPEED, 0)

    def draw(self):
        screen.blit(self.image, self.rect)


class Apple:
    """Falling apple object."""
    def __init__(self):
        self.image = apple_image
        self.rect = self.image.get_rect(topleft=(random.randint(50, SCREEN_WIDTH - TILESIZE), APPLE_SPAWN_Y))
        self.speed = random.choice(APPLE_FALL_SPEED)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


def reset_apple():
    """Spawn a new apple at a random position."""
    return Apple()


def update():
    """Update game logic."""
    global score, speed

    player.move()

    # Apple movement & collision detection
    for apple in apples[:]:
        apple.move()

        # If apple hits the floor, reset it
        if apple.rect.colliderect(floor_rect):
            apples.remove(apple)
            apples.append(reset_apple())

        # If player catches the apple
        elif apple.rect.colliderect(player.rect):
            apples.remove(apple)
            apples.append(reset_apple())
            score += 1
            speed = min(speed + 0.1, 6)  # Cap the speed increase
            pickup.play()


def draw():
    """Draw all elements to the screen."""
    screen.fill('lightblue')
    screen.blit(floor_image, floor_rect)
    
    player.draw()
    
    for apple in apples:
        apple.draw()

    # Display score
    score_text = font.render(f'Score: {score}', True, "white")
    screen.blit(score_text, (5, 5))


# Initialize game variables
player = Player()
apples = [reset_apple() for _ in range(APPLE_LIMIT)]
score = 0
speed = 3
running = True

# Game loop
while running:
    screen.fill('lightblue')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update()
    draw()
    
    pygame.display.update()
    clock.tick(60)
