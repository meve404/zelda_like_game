import pygame
from debug import debug
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        # Sprite setup
        self.create_map()
    
    def create_map(self):
        # To check the index and value of each list
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x': # Assigns a sprite to 'x'
                    Tile((x,y), [self.visible_sprites, self.obstacles_sprites])
                elif col == 'p': # Assigns a sprite to 'p'
                    Player((x,y), [self.visible_sprites])

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)
