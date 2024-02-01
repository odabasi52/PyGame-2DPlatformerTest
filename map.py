import pygame
from player import Player
from object import *
from os.path import join
WIDTH, HEIGHT = 1152, 720

class Map:
    # 24 - 15
    # X Block
    # P player1, B player2
    game_map = [
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X                      X",
        "X          X           X",
        "X   X                  X",
        "X    X                 X",
        "X    X  X   P F  B     X",
        "XXXXXXXXXXXXXXXXXXXXXXXX",
    ]
    def __init__(self, color):
        self.color = color
    
    def get_background(self):
        image = pygame.image.load(join("assets", "background", self.color + ".png"))
        _, _, width, height = image.get_rect()
        tiles_pos = []
        
        for x in range(WIDTH // width + 1):
            for y in range(HEIGHT // height + 1):
                pos = (x * width, y * height)
                tiles_pos.append(pos)
        return tiles_pos, image
    
    def draw_map(self, window, player1, player2, blocks):
        tiles_pos, bg_img = self.get_background()
        for tile in tiles_pos:
            window.blit(bg_img, tile)
        player1.draw(window)
        player2.draw(window)
        for block in blocks:
            block.draw(window)
        pygame.display.update()
        
    def create_map(self):
        player1 = None
        player2 = None
        blocks = []
        y = 0
        for row in self.game_map:
            x = 0
            for char in row:
                if char == "P":
                    player1 = Player(x, y, 0, 0, "NinjaFrog", True)
                elif char == "B":
                    player2 = Player(x, y, 0, 0, "VirtualGuy", False)
                elif char == "X":
                    blocks.append(Block(x, y, 48))
                elif char == "F":
                    fire = Fire(x + 16,y + 16, 16, 32)
                    blocks.append(fire)
                    fire.on()
                    fire.loop()
                x += 48
            y += 48
        
        return blocks, player1, player2