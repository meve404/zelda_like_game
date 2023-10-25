import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
    
    def move(self, speed):
        # Normalize the direction to avoid extra speed
        if self.direction.magnitude() != 0: # Vector of 0 cannot be normalized
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox): # Checks the rectangule of the sprite and rect of the player
                    if self.direction.x > 0: # Moving right
                        self.hitbox.right = sprite.hitbox.left

                    elif self.direction.x < 0: # Moving left
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox): # Checks the rectangule of the sprite and rect of the player
                    if self.direction.y > 0: # Moving down
                        self.hitbox.bottom = sprite.hitbox.top

                    elif self.direction.y < 0: # Moving up
                        self.hitbox.top = sprite.hitbox.bottom
