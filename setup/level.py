import pygame
from settings import *
from tile import Tile
from player import Player
from support import import_csv_layout, import_folder
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from debug import debug

class Level:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # Sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
    
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv'),
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
                        
                        elif style == 'entities':
                            if col == '394': # the id of the player
                                self.player = Player((x,y), [self.visible_sprites], 
                                                    self.obstacles_sprites, self.create_attack, 
                                                    self.destroy_attack, self.create_magic) # Passes the method to the Player class
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'

                                Enemy(monster_name, (x,y), [self.visible_sprites], self.obstacles_sprites)

        #         if col == 'x': # Assigns a sprite to 'x'
        #             Tile((x,y), [self.visible_sprites, self.obstacles_sprites])
        #         elif col == 'p': # Assigns a sprite to 'p'
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacles_sprites) 
    
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strenght, cost):
        print(style, '\n', strenght, '\n', cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        
        self.current_attack = None

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)

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

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
