import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
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
                    self.player = Player((x,y), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # Draws the sprites on a different spot

    def custom_draw(self, player):
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_postition =  sprite.rect.topleft - self.offset # Creates a camera by drawing the sprites where the player is
            self.display_surface.blit(sprite.image, offset_postition)