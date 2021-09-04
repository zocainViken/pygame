import pygame
import math 

TILE = 50
HEIGHT = 400
DOUBLE_HEIGHT = 2 * HEIGHT
HALF_HEIGHT = HEIGHT // 2
WIDTH = 600
HALF_WIDTH = WIDTH // 2


class Player():
    def __init__(self, x, y, collision_wall, sprites):
        self.x = x
        self.y = y

        #self.pos = (self.x, self.y)
        self.angle = 0
        self.speed = 2
        self.shot = False
        self.sensivity = 0.004

        self.collision_wall = collision_wall
        self.sprites = sprites
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in self.sprites.list_of_objects if obj.blocked]
        self.collision_list = self.collision_wall + self.collision_sprites

        self.side = 50
        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)
        
        #self.double_pi = 2 * math.pi

 
    @property
    def pos(self):
        return (self.x, self.y)

    #@property
    def collision_list(self):
         return self.collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in self.sprites.list_of_objects if obj.blocked]

    '''def collision_list(self):
        return self.collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in self.sprites.list_of_objects if obj.blocked]'''

    def collision_detection(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            print(len(hit_indexes))
            delta_x, delta_y = 0, 0
            for index in hit_indexes:
                hit_rect = self.collision_list[index]
                
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left

                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
        
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy


    def movement(self):
        double_pi = 2 * math.pi

        self.control_key()
        self.control_mouse()
        
        self.rect.center = self.x, self.y
        #self.pos = (self.x, self.y)
        self.angle %= double_pi

    def control_key(self):
        # capture1.png
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            #self.y -= self.speed
            dx = self.speed * cos_a
            dy = self.speed * sin_a
            self.collision_detection(dx, dy)
            #print('W')

        elif keys[pygame.K_s]:
            #self.y += self.speed
            dx = self.speed * cos_a
            dy = self.speed * sin_a
            self.collision_detection(dx, dy)
            #print('S')

        elif keys[pygame.K_a]:
            #self.x -= self.speed
            dx = self.speed * cos_a
            dy = self.speed * sin_a
            self.collision_detection(dx, dy)
            #print('A')

        elif keys[pygame.K_d]:
            #self.x += self.speed
            dx = self.speed * cos_a
            dy = self.speed * sin_a
            self.collision_detection(dx, dy)
            #print('D')

        elif keys[pygame.K_LEFT]:
            self.angle -= 0.04

        elif keys[pygame.K_RIGHT]:
            self.angle += 0.04
        
        elif keys[pygame.K_ESCAPE]:
            exit()
        

    def control_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensivity














































