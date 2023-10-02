import pygame
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout, import_folder
from random import choice
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
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects'),
        }

        # To check the index and value of each list
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x,y), [self.obstacles_sprites], 'invisible')
                        
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)

                        elif style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'object', surface)


        #         if col == 'x': # Assigns a sprite to 'x'
        #             Tile((x,y), [self.visible_sprites, self.obstacles_sprites])
        #         elif col == 'p': # Assigns a sprite to 'p'
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacles_sprites)
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites)
    
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # Draws the sprites on a different spot

        # Creating the floor
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft= (0,0))

    def custom_draw(self, player):
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        
        # Determines the drawing order of sprites based on their vertical positions
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_postition =  sprite.rect.topleft - self.offset # Creates a camera by drawing the sprites where the player is
            self.display_surface.blit(sprite.image, offset_postition)