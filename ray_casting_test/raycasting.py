import math
import pygame
from world import World

class RayCasting:
    def __init__(self, screen, half_height):
        world = World()
        self.tile = world.tile
        self.world_map = world.world_map

        self.screen = screen
        self.height = self.screen.get_height()
        self.half_height = half_height
        # capture2.png
        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_ray = 120
        self.max_depth = 800
        self.delta_angle = self.fov / self.num_ray
        self.dist = self.num_ray / (2 * math.tan(self.half_fov))
        self.projection_coefficient = 3 * self.dist * int(self.tile)
        self.scale = int(screen.get_width()) // self.num_ray

        '''# texture setting
        self.texture_width = 1200
        self.texture_height = 1200
        self.texture_scale = self.texture_width // self.tile'''


    def mapping(self, ox, oy):
        return (ox // self.tile) * self.tile, (oy // self.tile) * self.tile

    def ray_caster(self, screen, player_pos, player_angle, textures):
        # texture setting
        texture_width = 1200
        texture_height = 1200
        texture_scale = texture_width // self.tile

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
                y_v = oy + depth_v * sin_a
                tile_v = self.mapping(x + dx, y_v)
                if tile_v in self.world_map:
                    texture_v = self.world_map[tile_v]
                    break
                x += dx * self.tile
                
            # horizontals
            y, dy = (ym + self.tile, 1)if sin_a >= 0 else (ym, -1)
            for i in range(0, self.screen.get_height(), self.tile):
                depth_h = (y - oy) / sin_a
                x_h = ox + depth_h * cos_a
                tile_h = self.mapping(x_h, y + dy)
                if tile_h  in self.world_map:
                    texture_h = self.world_map[tile_h]
                    break
                y += dy * self.tile

            # projection
            depth, offset, texture = (depth_v, y_v, texture_v) if depth_v < depth_h else (depth_h, x_h, texture_h)
            offset = int(offset) % self.tile
            depth *= math.cos(player_angle - current_angle)
            depth = max(depth, 0.00001)
            projection_height = min(int(self.projection_coefficient / depth), self.height * 2)
            wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
            wall_column = pygame.transform.scale(wall_column, (self.scale, projection_height))
            screen.blit(wall_column, (ray * self.scale, self.half_height - projection_height // 2))
            '''c = 255 / (1 + depth * depth * 0.0002)
            color = (c, c//2, c//3)
            pygame.draw.rect(self.screen, color,
                            (ray * self.scale, self.half_height - projection_height // 2, self.scale, projection_height ))'''
            current_angle += self.delta_angle




















