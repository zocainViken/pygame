
from typing import Dict
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32


class World:
    def __init__(self):
        self.tile = 50# need to import it from game
        self.height = 400
        self.width = 600

        _ = False
        self.map = [
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                            [1, _, 2, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1], 
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1], 
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        ]
        '''self.map = [
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1], 
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
                            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1], 
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        ]'''
        self.world_width = len(self.map[0]) * self.tile
        self.world_height = len(self.map) * self.tile
        #self.world_map = {}
        self.world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        # mini map setting
        self.mini_map = set()# what is function set ?
        
        self.minimap_scale = 5
        self.minimap_res = (self.width // self.minimap_scale, self.height // self.minimap_scale)

        self.map_scale = 2 * self.minimap_scale
        self.map_tile = self.tile // self.map_scale
        self.map_pos = (0, self.height - self.height // self.minimap_scale)

        self.collision_wall = []
        
        for j, row in enumerate(self.map):
            for i, char in enumerate(row):
                if char:
                    self.mini_map.add((i * self.map_tile, j * self.map_tile))
                    self.collision_wall.append(pygame.Rect(i * self.tile, j * self.tile, self.tile, self.tile))
                    if char == 1:
                        self.world_map[(i * self.tile, j * self.tile)] = 1
                    elif char == 2:
                        self.world_map[(i * self.tile, j * self.tile)] = 2
                    elif char == 3:
                        self.world_map[(i * self.tile, j * self.tile)] = 3
                    elif char == 4:
                        self.world_map[(i * self.tile, j * self.tile)] = 4


class MiniMap:
    def __init__(self) -> None:
        self.world = World()
        self.map_scale = 5
        self.map_tile = self.world.tile // self.map_scale
        yellow = (250, 250, 0)
        self.minimap_scale = 5
        self.minimap_res = (600 // self.minimap_scale, 400 // self.minimap_scale)

        self.mini_map = set()
























