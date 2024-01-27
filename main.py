import pygame
from os.path import join

WIDTH, HEIGHT = 1280, 720
FPS = 60
SPEED = 5

pygame.init()
pygame.display.set_caption("Eda")
window = pygame.display.set_mode((WIDTH, HEIGHT))

from player import Player

def get_background(color):
    image = pygame.image.load(join("assets", "background", color))
    _, _, width, height = image.get_rect()
    tiles_pos = []
    
    for x in range(WIDTH // width + 1):
        for y in range(HEIGHT // height + 1):
            pos = (x * width, y * height)
            tiles_pos.append(pos)
    return tiles_pos, image

def draw(window, player):
    tiles_pos, bg_img = get_background("Blue.png")
    for tile in tiles_pos:
        window.blit(bg_img, tile)
    player.draw(window)
    pygame.display.update()

def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_x(SPEED, False)
    elif keys[pygame.K_d]:
        player.move_x(SPEED, True)    

def main(window):
    run = True
    clock = pygame.time.Clock()
    player = Player(100, 100, 50, 50)
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        player.loop(FPS)
        handle_move(player)
        draw(window, player)

    pygame.quit()
    exit()
            

if __name__ == "__main__":
    main(window)