import pygame

WIDTH, HEIGHT = 1152, 720
FPS = 60

pygame.init()
pygame.display.set_caption("Eda")
window = pygame.display.set_mode((WIDTH, HEIGHT))

from map import Map

def main(window):
    run = True
    clock = pygame.time.Clock()
    map = Map("Blue")
    objects, player1, player2, fire_traps = map.create_map()

    objects += fire_traps
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player1.jump_count < 2:
                    player1.jump()
                if event.key == pygame.K_UP and player2.jump_count < 2:
                    player2.jump()

        player1.loop(FPS)
        player2.loop(FPS)
        player1.handle_move(objects, player2)
        player2.handle_move(objects, player1)
        for fire in fire_traps:
            fire.on()
            fire.loop()
        map.draw_map(window, player1, player2, objects)

    pygame.quit()
    exit()
            

if __name__ == "__main__":
    main(window)