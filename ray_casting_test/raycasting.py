import math
import pygame
from world import World

class RayCasting:
    def __init__(self, screen, half_height):
        world = World()
        self.tile = world.tile
        self.world_map = world.world_map

        self.screen = screen
        self.half_height = half_height
        # capture2.png
        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_ray = 120
        self.max_depth = 800
        self.delta_angle = self.fov / self.num_ray
        self.dist = self.num_ray / (2 * math.tan(self.half_fov))
        self.projection_coefficient =self.dist * int(self.tile)
        self.scale = int(screen.get_width()) // self.num_ray

        

    '''def ray_caster(self, screen, player_pos, player_angle):
        current_angle = player_angle - self.half_fov
        x_origine, y_origine = player_pos

        for ray in range (self.num_ray):
            sin_a = math.sin(current_angle)
            cos_a = math.cos(current_angle)
            for depth in range(self.max_depth):
                x = x_origine + depth * cos_a
                y = y_origine + depth * sin_a
                #pygame.draw.line(screen, (50, 50, 50), player_pos, (x, y), 2)
                if (x // self.tile * self.tile, y // self.tile * self.tile) in self.world_map:
                    depth *= math.cos(player_angle - current_angle)
                    projection_height = self.projection_coefficient / depth
                    c = 255 / (1 + depth * depth * 0.0002)
                    color = (c, c//2, c//3)
                    pygame.draw.rect(self.screen, color,
                                    (ray * self.scale, self.half_height - projection_height // 2, self.scale, projection_height ))
                    break
            current_angle += self.delta_angle'''

    def mapping(self, ox, oy):
        return (ox // self.tile) * self.tile, (oy // self.tile) * self.tile

    def ray_caster(self, screen, player_pos, player_angle):
        # capture6.png --> 9
        ox, oy = player_pos
        xm, ym = self.mapping(ox, oy)
        current_angle = player_angle - self.half_fov

        for ray in range(self.num_ray):
            sin_a = math.sin(current_angle)
            cos_a = math.cos(current_angle)

            # verticals
            x, dx = (xm + self.tile, 1)if cos_a >= 0 else (xm, -1)
            for i in range(0, self.screen.get_height(), self.tile):
                depth_v = (x - ox) / cos_a
                y = oy + depth_v * sin_a
                if self.mapping(x + dx, y) in self.world_map:
                    break
                x += dx * self.tile
                
            # horizontals
            y, dy = (ym + self.tile, 1)if sin_a >= 0 else (ym, -1)
            for i in range(0, self.screen.get_height(), self.tile):
                depth_h = (y - oy) / sin_a
                x = ox + depth_h * cos_a
                if self.mapping(x, y + dy) in self.world_map:
                    break
                y += dy * self.tile

            # projection
            depth = depth_v if depth_v < depth_h else depth_h
            depth *= math.cos(player_angle - current_angle)
            projection_height = self.projection_coefficient / depth
            c = 255 / (1 + depth * depth * 0.0002)
            color = (c, c//2, c//3)
            pygame.draw.rect(self.screen, color,
                            (ray * self.scale, self.half_height - projection_height // 2, self.scale, projection_height ))
            current_angle += self.delta_angle




















