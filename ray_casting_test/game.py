# base from:
# https://www.youtube.com/watch?v=6FwR56UKlYU&list=PLzuEVvwBnAsZGeSVhOXpnW-ULsGYpNyQe&index=2&ab_channel=StandaloneCoder
# image from:
# https://github.com/StanislavPetrovV/Raycasting-3d-game-tutorial/tree/master/part%20%237
import pygame
import math
from player import Player
from world import World
#from raycasting import RayCasting
from drawing import Drawing
from sprite import *
from raycasting import ray_caster, ray_casting_walls
from interaction import Interaction

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
        self.world = World()
        self.sprites = Sprites()
        self.player = Player(int(self.half_width), int(self.half_height), self.world.collision_wall, self.sprites)# mini map screen
        self.mini_screen = pygame.Surface(self.world.minimap_res)
        self.draw = Drawing(self.screen, self.mini_screen, self.player, self.clock)
        self.interaction = Interaction(self.player, self.sprites, self.draw, self.world.world_map)

        


    def run(self):
        # launch start menu
        self.draw.menu()
        
        #blue_sky = (2, 120, 245)
        pygame.mouse.set_visible(False)
        run = True
    
        # play main theme music
        #self.interaction.play_music()

        while run:
            self.player.movement()

            # drawing our sky
            self.draw.background(self.player.angle)
           
            # draw our ray casting
            #walls = self.ray_casting.ray_caster(self.player, self.draw.textures)
            player_pos = (self.player.x, self.player.y)
            walls, wall_shot = ray_casting_walls(player_pos, self.player.angle, self.draw.textures, self.world.world_map, self.world.world_width, self.world.world_height)
            self.draw.world(walls + [obj.object_locate(self.player) for obj in self.sprites.list_of_objects ])

            # draw player weapon
            self.draw.player_weapon([wall_shot, self.sprites.sprite_shot])
            # draw our fps
            self.draw.fps(self.clock)

            # draw mini map
            self.draw.mini_map(self.player)

            self.interaction.interaction_object()
            self.interaction.npc_action()
            self.interaction.clear_world()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.player.shot:
                        self.player.shot = True
            
            pygame.display.update()
            self.clock.tick(self.FPS)
            #self.clock.tick()


        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()