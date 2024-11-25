import os
import json
import pygame
from pygame.locals import *

# Screen dimensions
SCREEN_WIDTH = 32*16
SCREEN_HEIGHT = 24*16
TILE_SIZE = 16  # Based on your JSON configuration

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, is_collidable=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_collidable = is_collidable  # Whether this tile is collidable or not

    def update(self):
        # You can add any logic here that you want to happen every frame for the tiles
        pass


class Tilemap:
    @staticmethod
    def load_tileset_images(tilesets):
        """
        Load tileset images and create a mapping from GID to tile images.
        """
        gid_to_image = {}
        for tileset in tilesets:
            first_gid = tileset["firstgid"]
            tsx_path = tileset["source"]
            tsx_dir = os.path.dirname(tsx_path)

            # Parse the TSX file to get the tileset image path
            with open(tsx_path, "r") as tsx_file:
                tsx_data = tsx_file.read()
                image_source = tsx_data.split('source="')[1].split('"')[0]
                image_path = os.path.join(tsx_dir, image_source)

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Tileset image not found: {image_path}")

            # Load the tileset image
            tileset_image = pygame.image.load(image_path).convert_alpha()
            tileset_width = tileset_image.get_width() // TILE_SIZE
            tileset_height = tileset_image.get_height() // TILE_SIZE

            # Slice the tileset image into individual tiles
            for tile_y in range(tileset_height):
                for tile_x in range(tileset_width):
                    gid = first_gid + tile_y * tileset_width + tile_x
                    rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    gid_to_image[gid] = tileset_image.subsurface(rect)

        return gid_to_image

    @staticmethod
    def create_sprite_groups(layers, gid_to_image):
        """
        Create sprite groups for different layers (including collidable tiles).
        """
        all_sprites = pygame.sprite.Group()
        collidables = pygame.sprite.Group()

        for layer in layers:
            if layer["type"] == "tilelayer" and layer["visible"]:
                width = layer["width"]
                height = layer["height"]
                data = layer["data"]

                # Check if the layer is for collidables
                is_collidable_layer = layer.get("name") == "Collidables"  # Or whatever layer name you use

                for y in range(height):
                    for x in range(width):
                        gid = data[y * width + x]
                        if gid != 0:  # Non-empty tile
                            tile_image = gid_to_image.get(gid)
                            if tile_image:
                                # Create a tile sprite
                                tile_sprite = Tile(tile_image, x * TILE_SIZE, y * TILE_SIZE, is_collidable_layer)

                                # Add to the appropriate sprite group
                                all_sprites.add(tile_sprite)
                                if is_collidable_layer:
                                    collidables.add(tile_sprite)

        return all_sprites, collidables

    @staticmethod
    def load_tilemap(file_path):
        """
        Load a tilemap from a JSON file.
        """
        with open(file_path, 'r') as json_file:
            tilemap_data = json.load(json_file)

        return tilemap_data


