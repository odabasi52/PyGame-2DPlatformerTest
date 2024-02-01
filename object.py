import pygame
from os.path import join
from player import load_sprites

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h) 
        self.width = w
        self.height = h
        self.img = pygame.Surface((w, h), pygame.SRCALPHA)
        self.name = name
        
    def draw(self, window):
        window.blit(self.img, (self.rect.x, self.rect.y))
              
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = self.get_block(size)
        self.img.blit(block, (0, 0)) 
        self.mask = pygame.mask.from_surface(self.img)

    def get_block(self, size):
        path = join("assets", "Terrain", "Terrain.png")
        img = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(0, 0, size, size)
        surface.blit(img, (0, 0), rect)
        return surface

class Fire(Object):
    ANIMATION_DELAY = 2
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "fire")
        self.fire_sprites = load_sprites("Traps", "Fire", w, h)
        self.img = self.fire_sprites["off"][0]
        self.mask = pygame.mask.from_surface(self.img)
        self.animation_count = 0
        self.animation_name = "off"
        
    def on(self):
        self.animation_name = "on"
    
    def off(self):
        self.animation_name = "off"
    
    def loop(self):
        sprites = self.fire_sprites[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.img = sprites[sprite_index]
        self.animation_count += 1
        
        self.rect = self.img.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.img)
        
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
    