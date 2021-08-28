# base from:
# https://www.youtube.com/watch?v=6FwR56UKlYU&list=PLzuEVvwBnAsZGeSVhOXpnW-ULsGYpNyQe&index=2&ab_channel=StandaloneCoder
# image from:
# https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/tree/master/part%20%237
import pygame
import math
from player import Player
from world import World
from raycasting import RayCasting
from drawing import Drawing
from sprite import *

class Game:
    def __init__(self) -> None:
        # screen variable
        width = 600
        height = 400
        self.width = 600
        self.height = 400
        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('doom')

        # some color variable
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (155, 155, 155)
        self.green = (0, 255, 255)

        # game variable
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.tile = 50
        

        # some import 
        self.player = Player(int(self.half_width), int(self.half_height))
        self.world = World()
        self.ray_casting = RayCasting(self.screen, self.half_height)
        self.sprites = Sprites()

        # mini map screen
        self.mini_screen = pygame.Surface((self.width // self.world.map_scale, self.height // self.world.map_scale))
        self.draw = Drawing(self.screen, self.mini_screen)


    def run(self):
        #blue_sky = (2, 120, 245)
        run = True
        
        while run:
            # draw bg color
            self.screen.fill(self.black)

            self.player.movement()

            # drawing our sky
            self.draw.background(self.player.angle)
           
            # draw our ray casting
            #self.draw.world(self.player.pos, self.player.angle)
            walls = self.ray_casting.ray_caster(self.player, self.draw.textures)
            
            self.draw.world(walls + [obj.object_locate(self.player, walls) for obj in self.sprites.list_objects ])

            # draw our fps
            self.draw.fps(self.clock)

            # draw mini map
            self.draw.mini_map(self.player)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            pygame.display.update()
            self.clock.tick(self.FPS)
            #self.clock.tick()


        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()