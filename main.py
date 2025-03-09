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
APPLE_SPAWN_Y = -50
APPLE_LIMIT = 3  # Max apples at once
MAX_LIVES = 3

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
big_font = pygame.font.Font('assets/PixeloidMono.ttf', TILESIZE)

# Sound Effects
pickup = pygame.mixer.Sound('assets/powerup.mp3')
pickup.set_volume(0.2)

game_over_sound = pygame.mixer.Sound('assets/powerup.mp3')
game_over_sound.set_volume(0.3)


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
    def __init__(self, speed):
        self.image = apple_image
        self.rect = self.image.get_rect(topleft=(random.randint(50, SCREEN_WIDTH - TILESIZE), APPLE_SPAWN_Y))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


def reset_apples(speed):
    """Spawn new apples with increasing speed."""
    return [Apple(speed) for _ in range(APPLE_LIMIT)]


def reset_game():
    """Reset all game variables."""
    global score, speed, lives, apples, game_over, started
    score = 0
    speed = 3
    lives = MAX_LIVES
    apples = reset_apples(speed)
    game_over = False
    started = True


def show_text(text, y_offset=0, color="white", font_size="big"):
    """Display centered text on the screen."""
    used_font = big_font if font_size == "big" else font
    text_surface = used_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(text_surface, text_rect)


def update():
    """Update game logic."""
    global score, speed, lives, game_over

    if game_over:
        return

    player.move()

    for apple in apples[:]:
        apple.move()

        # If apple hits the floor (missed)
        if apple.rect.colliderect(floor_rect):
            apples.remove(apple)
            apples.append(Apple(speed))
            lives -= 1

            if lives <= 0:
                game_over_sound.play()
                game_over = True

        # If player catches the apple
        elif apple.rect.colliderect(player.rect):
            apples.remove(apple)
            apples.append(Apple(speed))
            score += 1
            speed = min(speed + 0.1, 6)  # Gradually increase speed, capped
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

    # Display lives as hearts
    for i in range(lives):
        pygame.draw.circle(screen, "red", (SCREEN_WIDTH - 20 - i * 20, 15), 7)

    # Display Game Over screen
    if game_over:
        show_text("GAME OVER", -30, "red")
        show_text("Press SPACE to Restart", 30, "white", "small")


# Initialize game variables
player = Player()
apples = reset_apples(3)
score = 0
speed = 3
lives = MAX_LIVES
game_over = False
started = False

# Game loop
while True:
    screen.fill('lightblue')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()

    if not started:
        show_text("Press SPACE to Start", 0)
    else:
        update()
        draw()

    pygame.display.update()
    clock.tick(60)
