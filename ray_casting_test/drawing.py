
import pygame
import math

from raycasting import RayCasting
from world import World

class Drawing():
    def __init__(self, screen, mini_screen) -> None:
        self.screen = screen 
        self.mini_screen = mini_screen

        self.world_ = World()
        self.map_scale = self.world_.map_scale
        self.world_map = self.world_.mini_map
        self.tile = self.world_.tile

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.mini_map_pos = (0, self.height - self.height // self.map_scale)

        # some color variable
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (155, 155, 155)
        self.green = (0, 255, 255)
        self.yellow = (250, 250, 0)
        self.red = (250, 0, 0)
        self.sandy = (244, 164, 96)

        # load some texture
        self.textures = {'1' : pygame.image.load('img/wall1.png').convert_alpha(),
                        '2' : pygame.image.load('img/wall2.png').convert_alpha(),
                        '3' : pygame.image.load('img/wall3.png').convert_alpha(),
                        'S' : pygame.image.load('img/sky3.png').convert_alpha(),}

        self.ray_casting = RayCasting(self.screen, int(self.screen.get_height()) / 2)
        self.font = pygame.font.SysFont('Arial', 32, bold = True)
        

    def background(self, angle):
        '''blue_sky = (2, 120, 245)
        # draw our sky
        pygame.draw.rect(self.screen, blue_sky, (0, 0, self.width, int(self.screen.get_height()) / 2))'''

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
            pygame.draw.rect(self.mini_screen, (152, 41, 3), (x, y, self.tile//ratio, self.tile//ratio) )
        self.screen.blit(self.mini_screen, self.mini_map_pos)








