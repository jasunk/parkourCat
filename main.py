import os
import json
import pygame
from pygame.locals import *
from klasser.tilemap import Tilemap
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 32*16
SCREEN_HEIGHT = 24*16
TILE_SIZE = 16  # Based on your JSON configuration




# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tilemap Game")

# Create a clock to control frame rate
clock = pygame.time.Clock()

# Load the JSON tilemap and tilesets (assuming `tilemap.json` and tilesets are correctly set)
with open("grafikk/assets/test.json") as f:
    tilemap_data = json.load(f)

# Load tilesets and create the GID to image mapping
tilesets = tilemap_data["tilesets"]
gid_to_image = Tilemap.load_tileset_images(tilesets)

# Create sprite groups for the different layers
all_sprites, collidables = Tilemap.create_sprite_groups(tilemap_data["layers"], gid_to_image)

# Example Player (add your player code here)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))  # Red color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Create player instance
player = Player()
all_sprites.add(player)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Collision with collidables (assuming you have collision logic with collidables)
    if not pygame.sprite.spritecollide(player, collidables, False):
        player.rect.y+=5

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen
    all_sprites.draw(screen)  # Draw all sprites (tiles and player)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()