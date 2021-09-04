

from collections import deque
import pygame
import math

from pygame import transform
from random import randrange
import sys
from setting import BLACK, WIDTH, HEIGHT, HALF_HEIGHT, HALF_WIDTH

#from raycasting import RayCasting
from world import World

class Drawing():
    def __init__(self, screen, mini_screen, player, clock) -> None:
        self.screen = screen 
        self.mini_screen = mini_screen
        self.player = player
        self.clock = clock

        # start menu game
        self.menu_trigger = True
        menu_picture = pygame.image.load('img/bg.jpg')
        self.menu_picture = pygame.transform.scale(menu_picture, (int(WIDTH*2), HEIGHT))

        self.world_ = World()
        self.map_scale = self.world_.map_scale
        self.world_map = self.world_.mini_map
        self.tile = self.world_.tile
        self.map_tile = self.tile // self.map_scale

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.mini_map_pos = self.world_.map_pos

        # some color variable
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (155, 155, 155)
        self.green = (0, 255, 255)
        self.yellow = (250, 250, 0)
        self.red = (250, 0, 0)
        self.sandy = (244, 164, 96)

        # load some texture
        self.textures = {1 : pygame.image.load('img/wall1.png').convert_alpha(),
                         2 : pygame.image.load('img/wall2.png').convert_alpha(),
                         3 : pygame.image.load('img/wall3.png').convert_alpha(),
                         4 : pygame.image.load('img/wall4.png').convert_alpha(),
                        'S' : pygame.image.load('img/sky3.png').convert_alpha(),}
        
        self.font = pygame.font.SysFont('Arial', 32, bold = True)
        self.victory_font = pygame.font.SysFont('font/font.ttf', 144)

        # weapon_parameter
        picture_gun = pygame.image.load('sprites/weapons/shotgun/base/0.png').convert_alpha()
        picture_width = picture_gun.get_width()
        picture_height = picture_gun.get_height()
        self.weapon_basic_sprite = pygame.transform.scale(picture_gun, (picture_width//2, picture_height//2))
        
        self.weapon_shot_animation = deque([pygame.transform.scale(pygame.image.load(f'sprites/weapons/shotgun/shot/{i}.png').convert_alpha(), (picture_width//2, picture_height//2)) for i in range(20)])
        self.weapon_rect = self.weapon_basic_sprite.get_rect()
        self.weapon_position = (self.width // 2 - self.weapon_rect.width // 2, self.height - self.weapon_rect.height)
        
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('sound/shotgun.wav')

        # fx parameter
        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(0, 9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)
        

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % self.width
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - self.width, 0))
        self.screen.blit(self.textures['S'], (sky_offset + self.width, 0))
        
        # draw our floor
        pygame.draw.rect(self.screen, self.sandy, (0, int(self.screen.get_height()) / 2, self.width, int(self.screen.get_height()) / 2))

    def world(self, world_object):
        for obj in sorted(world_object, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, (217, 133, 4))
        self.screen.blit(render, (self.width - 65, 5))

    def mini_map(self, player):
        ratio = 5
        self.mini_screen.fill(self.black)
        mapx, mapy = player.x // self.map_scale, player.y // self.map_scale
        #draw player
        pygame.draw.circle(self.mini_screen, (84, 233, 4), (mapx, mapy), 3)
        pygame.draw.line(self.mini_screen, self.yellow, (mapx, mapy),
                        (mapx + 13 * math.cos(player.angle),
                         mapy + 13 * math.sin(player.angle) ))

        # draw world*
        for x, y in self.world_map:
            pygame.draw.rect(self.mini_screen, (152, 41, 3), (x, y, self.map_tile, self.map_tile) )
        self.screen.blit(self.mini_screen, self.mini_map_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1 
            self.sfx.rotate(-1)

    def player_weapon(self, shot_list):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shot_list)[1]// 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon_position)
            self.shot_animation_count += 1

            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        
        else:
            self.screen.blit(self.weapon_basic_sprite, self.weapon_position)

    def win(self):
        render = self.victory_font.render('YOU WIN !!!', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 500, 150)
        rect.center = HALF_WIDTH, HALF_HEIGHT
        pygame.draw.rect(self.screen, self.black, rect, border_radius = 50)
        self.screen.blit(render, (rect.centerx - 215, rect.centery - 70))

    def menu(self):
        x = 0
        button_font = pygame.font.Font('font/font.ttf', 50)
        label_font = pygame.font.Font('font/font1.otf', 200)
        start = button_font.render('START', 1, pygame.Color('lightgray'))
        button_start = pygame.Rect(0, 0, 200, 75)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 200, 75)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 100

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menu_picture, (0, 100), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            x += 1

            pygame.draw.rect(self.screen, BLACK, button_start, border_radius=25, width=10)
            self.screen.blit(start, (button_start.centerx - 90, button_start.centery - 50))

            pygame.draw.rect(self.screen, BLACK, button_exit, border_radius=25, width=10)
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 50))

            color = randrange(40)
            label = label_font.render('DOOMPy', 1, (color, color, color))
            self.screen.blit(label, (15, -30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLACK, button_start, border_radius=25)
                self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLACK, button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)


