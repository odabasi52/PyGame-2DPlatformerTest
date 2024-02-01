import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_charactes_assets()
        # variables to animate the player
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = "idle"
        self.facing_right = True
        # create a surface
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        # player movement
        self.direction = pygame.math.Vector2(0, 0)  # no movement initially because (x, y) is set to (0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
    
    def import_charactes_assets(self):
        character_path = "graphics/character/"
        self.animations = {"idle":[], "run":[], "jump":[], "fall":[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        if self.facing_right:
            self.image = animation[int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)
    
    def get_input(self):
        # get the pressed keys 
        keys = pygame.key.get_pressed()
        # x axis
        if keys[pygame.K_RIGHT]:
            self.facing_right = True
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.facing_right = False
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.direction.y == 0:
            self.jump()
    
    def get_status(self):
        self.status = "idle"
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > self.gravity:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
            
    def update(self):
        # get keyboard input
        self.get_input()
        # get player status
        self.get_status()
        # animate the player
        self.animate()