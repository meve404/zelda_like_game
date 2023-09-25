import pygame
from debug import debug
from settings import WORLD_MAP

class Level:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        # Sprites setup
        self.create_map()
    
    def create_map(self):
        for row in WORLD_MAP:
            print(row)

    def run(self):
        # update and draw the game
        pass
