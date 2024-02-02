import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # create a surface 
        self.image = pygame.Surface((size, size))
        self.image.fill("brown")
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
        # move the blocks horizontally (yatay)
        self.rect.x += x_shift
        