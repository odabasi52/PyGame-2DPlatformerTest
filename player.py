import pygame
from os import listdir
from os.path import isfile, join

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprites(dir1, dir2, w, h, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // w):
            surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i* w, 0, w, h)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites

class Player(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3
    GRAVITY = 1
    SPRITES = load_sprites("MainCharacters", "NinjaFrog", 32, 32, True)

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_x(self, vel, right):
        self.x_vel = vel if right else -vel
        
        if self.direction != "left" and self.x_vel < 0:
            self.direction = "left"
            self.animation_count = 0
            
        elif self.direction != "right" and self.x_vel > 0:
            self.direction = "right"
            self.animation_count = 0
            
    def loop(self, fps):
        #self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        self.update_sprite()
        
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"
            
        sprites = self.SPRITES[f"{sprite_sheet}_{self.direction}"]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, window): 
        window.blit(self.sprite, (self.rect.x, self.rect.y))
