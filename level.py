import pygame
from tiles import Tile
from player import Player
from settings import tile_size, screen_width

class Level:
    def __init__(self, level_map, screen):
        self.display_surface = screen
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        # X: Tile P: Player transformation
        self.setup_level(level_map)
        self.x_shift = 0
        self.current_x = 0 

    def setup_level(self, level_map):
        for row_index, row in enumerate(level_map):
            for col_index, col in enumerate(row):
                # position (x, y)
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    self.tiles.add(Tile((x, y), tile_size))
                elif col == 'P':
                    self.player.add(Player((x, y)))
                    
    def scroll_x(self):
        # retrieve the single sprite contained within the self.player group
        player = self.player.sprite
        # x-coordinate of the center point of the player sprite's bounding rectangle
        player_x = player.rect.centerx
        # x-coordinate of the player sprite's direction vector
        direction_x = player.direction.x
        # if player is on the left edge of the map and pressing left arrow key
        if player_x < screen_width / 4 and direction_x < 0:
            self.x_shift = 8
            player.speed = 0
        # if player is on the right edge of the map and pressing right arrow key
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.x_shift = -8
            player.speed = 0
        else:
            self.x_shift = 0
            player.speed = 8
            
    def horizontal_movement_collision(self):
        player = self.player.sprite
        # move the player according to it's speed
        player.rect.x += player.direction.x * player.speed
        # look through all the blocks
        for tile in self.tiles.sprites():
            # check if any of them collide with the player
            if tile.rect.colliderect(player.rect):
                # player going left
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                # player going right
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.rect.y += player.direction.y
        player.apply_gravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                # player going downwards
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                # player going upwards
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = player.gravity
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
                    
    def run(self):
        # map blocks (tiles)
        self.tiles.update(self.x_shift)
        self.scroll_x()
        self.tiles.draw(self.display_surface)
        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.display_surface.blit(self.player.sprite.image, self.player.sprite.rect) 
    