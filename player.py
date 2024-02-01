import pygame
from os import listdir
from os.path import isfile, join

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprites(dir1, dir2, w, h, direction=False, scale_by=1):
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
            sprites.append(pygame.transform.scale_by(surface, scale_by))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites


class Player(pygame.sprite.Sprite):
    SPEED = 3
    ANIMATION_DELAY = 2
    GRAVITY = 1
    

    def __init__(self, x, y, w, h, name, player1):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.name = name
        self.SPRITES = load_sprites("MainCharacters", self.name, 32, 32, True)
        self.player1 = player1
        self.max_hp = 100
        self.hp = self.max_hp
        
    def handle_vertical_collision(self, objs, dy, other):
        collided_objs = []
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                if dy > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed()
                elif dy < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head()
                collided_objs.append(obj)
        if pygame.sprite.collide_mask(self, other):
                if dy > 0:
                    self.rect.bottom = other.rect.top
                    self.landed()
                elif dy < 0:
                    self.rect.top = other.rect.bottom
                    self.hit_head()
                collided_objs.append(other)
                
        return collided_objs

    def handle_horizontal_collision(self, objs, dx, other):
        self.move(dx, 0)
        self.update()
        collided_obj = None
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                collided_obj = obj

        if pygame.sprite.collide_mask(self, other):
            collided_obj = other
             
        self.move(-dx, 0)
        self.update()
        return collided_obj

    def get_input(self):
        keys = pygame.key.get_pressed()
        if self.player1: 
            if keys[pygame.K_a]:
                return "L"
            elif keys[pygame.K_d]:
                return "R"
        else:
            if keys[pygame.K_LEFT]:
                return "L"
            elif keys[pygame.K_RIGHT]:
                return "R"

    def handle_move(self, objects, other):
        if self.hp > 0:
            self.x_vel = 0
            
            left_collide = self.handle_horizontal_collision(objects, -self.SPEED * 2, other)
            right_collide = self.handle_horizontal_collision(objects, self.SPEED * 2, other)
            key = self.get_input()
            if key == "L" and not left_collide:
                self.move_x(self.SPEED, False)
            elif key == "R" and not right_collide:
                self.move_x(self.SPEED, True)

            verts = self.handle_vertical_collision(objects, self.y_vel, other)
            collideds = [*verts, left_collide, right_collide]
            for o in collideds:
                if o and o.name == "fire":
                    self.get_hit()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel = -self.y_vel
        
    def jump(self):
        if self.hp > 0:
            self.jump_count += 1
            self.animation_count = 0
            self.y_vel = -self.GRAVITY * 6
            if self.jump_count == 1:
                self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_x(self, vel, right):
        self.x_vel = vel if right else -vel
        
        if self.direction != "left" and not right:
            self.direction = "left"
            self.animation_count = 0
            
        elif self.direction != "right" and right:
            self.direction = "right"
            self.animation_count = 0

    def get_hit(self):
        self.hit = True
        self.hit_count += 1
        self.hp -= 5
        if self.hp <= 0:
            self.animation_count = 0   
            
    def loop(self, fps):
        if self.hp > 0:
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
            self.move(self.x_vel, self.y_vel)
            
            if self.hit:
                self.hit_count += 1
            if self.hit_count >= fps:
                self.hit_count = 0
                self.hit = False
                
            self.fall_count += 1
            self.update_sprite()
        else:
            self.x_vel = 0
            self.y_vel = 0
            if self.animation_count < 14:
                self.play_dead_anim()
            else:
                self.rect.x = -500
                self.rect.y = -500

            
    def play_dead_anim(self):
        sprites = load_sprites("MainCharacters", "", 96, 96, False, 1/3)["Desappearing (96x96)"]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        
    def update_sprite(self):
        sprite_sheet = "idle"

        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
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
        ratio = self.hp / self.max_hp
        pygame.draw.rect(window, "red",(self.rect.x, self.rect.y - 8, 32, 6) )
        pygame.draw.rect(window, "green",(self.rect.x, self.rect.y - 8, 32 * ratio, 6) )
