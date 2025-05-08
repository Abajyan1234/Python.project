import pygame
import os
import math
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 200, 0)
DARK_RED = (200, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Create assets directory
if not os.path.exists('assets'):
    os.makedirs('assets')

def create_player():
    # Create player airplane with adjusted proportions
    surface = pygame.Surface((120, 80), pygame.SRCALPHA)  # Increased size
    
    # Draw main body (airplane shape)
    # Fuselage
    pygame.draw.rect(surface, GRAY, (50, 25, 30, 40))
    # Nose
    pygame.draw.polygon(surface, GRAY, [(80, 30), (110, 45), (80, 60)])
    # Tail
    pygame.draw.polygon(surface, GRAY, [(50, 25), (30, 15), (50, 15)])
    # Main wings (larger and more swept back)
    pygame.draw.polygon(surface, BLUE, [(20, 40), (100, 40), (60, 25)])
    # Tail wings (proportionally sized)
    pygame.draw.polygon(surface, BLUE, [(40, 15), (60, 15), (50, 10)])
    # Windows (multiple windows)
    for i in range(3):
        y_pos = 40 + i * 10
        pygame.draw.circle(surface, WHITE, (65, y_pos), 4)
        pygame.draw.circle(surface, BLACK, (65, y_pos), 4, 1)
    
    # Engine glow (larger and more detailed)
    pygame.draw.polygon(surface, YELLOW, [(85, 45), (105, 45), (95, 40), (95, 50)])
    pygame.draw.polygon(surface, ORANGE, [(85, 45), (105, 45), (95, 40), (95, 50)], 1)
    
    # Save image
    pygame.image.save(surface, 'assets/player.png')

def create_enemy():
    # Create enemy airplane with adjusted proportions
    surface = pygame.Surface((120, 80), pygame.SRCALPHA)  # Increased size
    
    # Draw main body (airplane shape)
    # Fuselage
    pygame.draw.rect(surface, GRAY, (50, 25, 30, 40))
    # Nose
    pygame.draw.polygon(surface, GRAY, [(50, 30), (30, 45), (50, 60)])
    # Tail
    pygame.draw.polygon(surface, GRAY, [(80, 25), (100, 15), (80, 15)])
    # Main wings (larger and more swept back)
    pygame.draw.polygon(surface, RED, [(20, 25), (100, 25), (60, 40)])
    # Tail wings (proportionally sized)
    pygame.draw.polygon(surface, RED, [(70, 15), (90, 15), (80, 10)])
    # Windows (multiple windows)
    for i in range(3):
        y_pos = 40 + i * 10
        pygame.draw.circle(surface, WHITE, (65, y_pos), 4)
        pygame.draw.circle(surface, BLACK, (65, y_pos), 4, 1)
    
    # Engine glow (larger and more detailed)
    pygame.draw.polygon(surface, YELLOW, [(35, 45), (15, 45), (25, 40), (25, 50)])
    pygame.draw.polygon(surface, ORANGE, [(35, 45), (15, 45), (25, 40), (25, 50)], 1)
    
    # Save image
    pygame.image.save(surface, 'assets/enemy.png')

def create_bullet(is_player=True):
    # Create bullet with trail effect
    surface = pygame.Surface((20, 40), pygame.SRCALPHA)  # Increased size
    
    # Draw bullet body
    color = BLUE if is_player else RED
    dark_color = (0, 0, 150) if is_player else DARK_RED
    pygame.draw.rect(surface, color, (0, 0, 20, 40))
    pygame.draw.rect(surface, dark_color, (0, 0, 20, 40), 2)
    
    # Draw bullet tip
    pygame.draw.polygon(surface, WHITE, [(0, 0), (20, 0), (10, -10)])
    
    # Draw trail
    for i in range(4):  # Increased trail length
        alpha = 100 - i * 25
        trail_color = (*color[:3], alpha)
        pygame.draw.rect(surface, trail_color, (0, 40 + i * 5, 20, 5))
    
    # Save image
    filename = 'bullet.png' if is_player else 'enemy_bullet.png'
    pygame.image.save(surface, f'assets/{filename}')

def create_firework():
    # Create firework explosion
    surface = pygame.Surface((120, 120), pygame.SRCALPHA)  # Increased size
    
    # Draw explosion particles
    colors = [RED, ORANGE, YELLOW, PURPLE]
    for i in range(30):  # More particles
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(20, 50)  # Increased range
        x = 60 + math.cos(angle) * distance
        y = 60 + math.sin(angle) * distance
        color = random.choice(colors)
        size = random.randint(2, 4)  # Varying sizes
        pygame.draw.circle(surface, color, (int(x), int(y)), size)
    
    # Save image
    pygame.image.save(surface, 'assets/firework.png')

if __name__ == '__main__':
    create_player()
    create_enemy()
    create_bullet(True)  # Player bullet
    create_bullet(False)  # Enemy bullet
    create_firework()