# base from:
# https://www.youtube.com/watch?v=6FwR56UKlYU&list=PLzuEVvwBnAsZGeSVhOXpnW-ULsGYpNyQe&index=2&ab_channel=StandaloneCoder

import pygame
import math
from player import Player
from world import World
from raycasting import RayCasting
from drawing import Drawing

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

        # mini map screen
        self.mini_screen = pygame.Surface((self.width // self.world.map_scale, self.height // self.world.map_scale))
        self.draw = Drawing(self.screen, self.mini_screen)


    def run(self):
        #blue_sky = (2, 120, 245)
        run = True
        
        while run:
            # draw bg color
            self.screen.fill(self.black)
            '''# draw player
            #                   where       color       position        radius
            pygame.draw.circle(self.screen, self.green, self.player.pos, 12)
            # capture.png explanation
            pygame.draw.line(self.screen, self.green, self.player.pos,
                            (self.player.x + self.width * math.cos(self.player.angle),
                             self.player.y + self.width * math.sin(self.player.angle) ))'''
            self.player.movement()

            # drawing our sky
            self.draw.background()
            '''# draw our sky
            pygame.draw.rect(self.screen, blue_sky, (0, 0, self.width, self.half_height))
            # draw our floor
            pygame.draw.rect(self.screen, (50, 50, 50), (0, self.half_height, self.width, self.half_height))'''
            
            # draw our ray casting
            #self.ray_casting.ray_caster(self.screen, self.player.pos, self.player.angle)
            self.draw.world(self.player.pos, self.player.angle)

            # draw our fps
            self.draw.fps(self.clock)
            self.draw.mini_map(self.player)



            '''# draw world*
            for x, y in self.world.world_map:
                pygame.draw.rect(self.screen, self.gray, (x, y, self.tile, self.tile), 2 )'''
            ''' #draw player
            pygame.draw.circle(self.screen, self.green, self.player.pos, 12)
            # draw where I face
            pygame.draw.line(self.screen, self.green, self.player.pos,
                            (self.player.x + self.width * math.cos(self.player.angle),
                             self.player.y + self.width * math.sin(self.player.angle) ))'''

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