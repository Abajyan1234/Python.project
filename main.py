# Essential Imports
import pygame
import random
import math
import os
from pygame import mixer
from game_data import GameData
import time

# Initialize Pygame and mixer for sound
pygame.init()
mixer.init()

# Initialize game data
game_data = GameData()
settings = game_data.get_settings()

# Game window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60  # Frames per second

# Define common colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

# Load Sounds (with error handling)
shoot_sound = None
powerup_sound = None
enemy_shoot_sound = None
try:
    shoot_sound = mixer.Sound('sounds/shoot.wav')
    shoot_sound.set_volume(settings["sound_volume"])
    powerup_sound = mixer.Sound('sounds/powerup.wav')
    powerup_sound.set_volume(settings["sound_volume"])
    enemy_shoot_sound = mixer.Sound('sounds/enemy_shoot.wav')
    enemy_shoot_sound.set_volume(settings["sound_volume"])
except:
    print("Warning: Sounds not loaded correctly.")

# Load image helper function
# If image not found, returns a colored rectangle fallback

def load_image(name, fallback_color=(255, 255, 255), size=(50, 40)):
    path = os.path.join('assets', name)
    if os.path.exists(path):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    else:
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface

# Load background image
background_img = load_image('background.jpg', fallback_color=(0, 0, 30), size=(WIDTH, HEIGHT))

# Background starfield class for aesthetic effect
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)
        self.color = (255, 255, 255)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

stars = [Star() for _ in range(100)]  # Create 100 background stars

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('player.png', fallback_color=BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 8
        self.health = 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.shoot_power = 1
        self.bullet_spread = 0
        self.shield_active = False
        self.shield_time = 0

    def update(self):
        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        # Shooting
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()

        # Shield timer
        if self.shield_active:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.shield_active = False

    def shoot(self):
        # Shoot single or multiple bullets depending on power level
        if self.shoot_power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        else:
            spread_step = self.bullet_spread / (self.shoot_power - 1)
            start_angle = -self.bullet_spread / 2
            for i in range(self.shoot_power):
                angle = start_angle + i * spread_step
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bullet.speedx = math.sin(math.radians(angle)) * 5
                all_sprites.add(bullet)
                bullets.add(bullet)
        if shoot_sound:
            shoot_sound.play()

    def apply_powerup(self, powerup_type):
        if powerup_sound:
            powerup_sound.play()
        if powerup_type == 'MULTI_SHOT':
            self.shoot_power = min(self.shoot_power + 1, 5)
            self.bullet_spread = 30
        elif powerup_type == 'SPEED_BOOST':
            self.speed = min(15, self.speed + 2)
        elif powerup_type == 'SHIELD':
            self.shield_active = True
            self.shield_time = 300

# Player bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('bullet.png', fallback_color=WHITE, size=(5, 15))
        self.rect = self.image.get_rect(center=(x, y))
        self.speedy = -10
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()

# Bullet fired by enemies
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('enemy.png', fallback_color=RED, size=(40, 30))
        self.rect = self.image.get_rect(x=random.randint(0, WIDTH - 40), y=random.randint(-100, -40))
        self.speedy = random.randint(2, 4)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1500, 3000)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            if enemy_shoot_sound:
                enemy_shoot_sound.play()

# Power-up class with random type
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['MULTI_SHOT', 'SPEED_BOOST', 'SHIELD'])
        self.color = PURPLE if self.type == 'MULTI_SHOT' else ORANGE if self.type == 'SPEED_BOOST' else CYAN
        self.image = pygame.Surface((20, 20))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(x=random.randint(0, WIDTH - 20), y=random.randint(-100, -40))
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Spawn initial enemies
for _ in range(6):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

# Load high score from file
record_path = "record.txt"
if os.path.exists(record_path):
    with open(record_path, 'r') as f:
        record = int(f.read())
else:
    record = 0

# Game variables
running = True
score = 0
level = 1
font = pygame.font.Font(None, 36)
start_time = time.time()
kills = 0

def show_game_over_screen(screen, score, level, game_data):
    screen.fill((0, 0, 30))  # Dark background
    
    # Load fonts
    title_font = pygame.font.Font(None, 74)
    text_font = pygame.font.Font(None, 36)
    
    # Game Over text
    game_over_text = title_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 50))
    
    # Final score
    score_text = text_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 150))
    
    # Level reached
    level_text = text_font.render(f"Level Reached: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 200))
    
    # High Scores
    high_scores = game_data.get_high_scores()
    high_score_text = text_font.render("High Scores:", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, 250))
    
    for i, score_data in enumerate(high_scores[:5]):  # Show top 5 scores
        score_line = text_font.render(
            f"{i+1}. {score_data['score']} (Level {score_data['level']}) - {score_data['date']}", 
            True, 
            WHITE
        )
        screen.blit(score_line, (WIDTH//2 - score_line.get_width()//2, 300 + i*30))
    
    # Stats
    stats = game_data.get_stats()
    stats_text = text_font.render("Game Statistics:", True, WHITE)
    screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, 500))
    
    # Format play time
    play_time = stats["total_play_time"]
    hours = int(play_time // 3600)
    minutes = int((play_time % 3600) // 60)
    seconds = int(play_time % 60)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    time_text = text_font.render(f"Total Play Time: {time_str}", True, WHITE)
    screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 530))
    
    kills_text = text_font.render(f"Total Kills: {stats['total_kills']}", True, WHITE)
    screen.blit(kills_text, (WIDTH//2 - kills_text.get_width()//2, 560))
    
    # Restart instructions
    restart_text = text_font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT - 50))
    
    pygame.display.flip()
    
    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

# Main game loop
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    for star in stars:
        star.update()

    # Bullet-enemy collision
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for _ in hits:
        score += 10
        kills += 1
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
        if random.random() < 0.2:
            p = PowerUp()
            all_sprites.add(p)
            powerups.add(p)

    # Player gets powerup
    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in powerup_hits:
        player.apply_powerup(hit.type)
        game_data.update_stats(0, 0, hit.type)

    # Enemy bullet hits player
    if pygame.sprite.spritecollide(player, enemy_bullets, True):
        if not player.shield_active:
            player.health -= 1
            if player.health <= 0:
                # Save game data
                play_time = time.time() - start_time
                game_data.update_stats(play_time, kills)
                game_data.add_high_score(score, level)
                
                # Show game over screen
                if not show_game_over_screen(screen, score, level, game_data):
                    running = False
                else:
                    # Reset game state
                    all_sprites = pygame.sprite.Group()
                    player = Player()
                    all_sprites.add(player)
                    bullets = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    powerups = pygame.sprite.Group()
                    enemy_bullets = pygame.sprite.Group()
                    score = 0
                    level = 1
                    kills = 0
                    start_time = time.time()
                    
                    # Spawn initial enemies
                    for _ in range(6):
                        e = Enemy()
                        all_sprites.add(e)
                        enemies.add(e)

    # Enemy collision with player
    if pygame.sprite.spritecollide(player, enemies, True):
        if not player.shield_active:
            player.health -= 1
            if player.health <= 0:
                # Save game data
                play_time = time.time() - start_time
                game_data.update_stats(play_time, kills)
                game_data.add_high_score(score, level)
                
                # Show game over screen
                if not show_game_over_screen(screen, score, level, game_data):
                    running = False
                else:
                    # Reset game state
                    all_sprites = pygame.sprite.Group()
                    player = Player()
                    all_sprites.add(player)
                    bullets = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    powerups = pygame.sprite.Group()
                    enemy_bullets = pygame.sprite.Group()
                    score = 0
                    level = 1
                    kills = 0
                    start_time = time.time()
                    
                    # Spawn initial enemies
                    for _ in range(6):
                        e = Enemy()
                        all_sprites.add(e)
                        enemies.add(e)

    # Level up logic
    if score > level * 100:
        level += 1
        player.shoot_power = min(player.shoot_power * 2, 8)
        player.bullet_spread = 30
        for _ in range(2):
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)

    # Drawing
    screen.blit(background_img, (0, 0))
    for star in stars:
        star.draw(screen)
    all_sprites.draw(screen)
    
    # Display high scores
    high_scores = game_data.get_high_scores()
    high_score_text = f"High Score: {high_scores[0]['score'] if high_scores else 0}"
    score_text = font.render(f"Score: {score}  Level: {level}  Health: {player.health}  {high_score_text}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.quit()