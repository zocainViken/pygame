import math
import pygame
from world import World
from numba import njit

'''
class RayCasting:
    def __init__(self, screen, half_height):
        world = World()
        self.tile = world.tile
        self.world_map = world.world_map
        self.world_width = world.world_width
        self.world_height = world.world_height

        self.screen = screen
        self.height = self.screen.get_height()
        self.half_height = half_height

        self.penta_height = 5 * self.height

        # capture2.png
        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_ray = 120
        self.max_depth = 800
        self.delta_angle = self.fov / self.num_ray
        self.dist = self.num_ray / (2 * math.tan(self.half_fov))
        self.projection_coefficient = 3 * self.dist * int(self.tile)
        self.scale = int(screen.get_width()) // self.num_ray


    #@njit(fastmath=True)
    def mapping(self, ox, oy):
        return (ox // self.tile) * self.tile, (oy // self.tile) * self.tile

    #def ray_caster(self, screen, player_pos, player_angle, textures):
    def ray_caster(self, player, textures):
        # texture setting
        texture_width = 1200
        texture_height = 1200
        texture_scale = texture_width // self.tile

        walls = []
        texture_v, texture_h = 1, 1

        # capture6.png --> 9
        ox, oy = player.pos
        xm, ym = self.mapping(ox, oy)
        current_angle = player.angle - self.half_fov

        for ray in range(self.num_ray):
            sin_a = math.sin(current_angle)
            cos_a = math.cos(current_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            # verticals
            x, dx = (xm + self.tile, 1)if cos_a >= 0 else (xm, -1)
            for i in range(0, self.world_width, self.tile):
                depth_v = (x - ox) / cos_a
                y_v = oy + depth_v * sin_a
                tile_v = self.mapping(x + dx, y_v)
                if tile_v in self.world_map:
                    texture_v = self.world_map[tile_v]
                    break
                x += dx * self.tile
                
            # horizontals
            y, dy = (ym + self.tile, 1)if sin_a >= 0 else (ym, -1)
            for i in range(0, self.world_height, self.tile):
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
            depth *= math.cos(player.angle - current_angle)
            depth = max(depth, 0.00001)
            projection_height = min(int(self.projection_coefficient / depth), self.penta_height)
            
            wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
            wall_column = pygame.transform.scale(wall_column, (self.scale, projection_height))
            
            wall_pos = (ray * self.scale, self.half_height - projection_height // 2)
            walls.append((depth, wall_column, wall_pos))
            
            current_angle += self.delta_angle

        return walls

'''


TILE = 50
WIDTH = 600
HEIGHT = 400
HALF_HEIGHT = HEIGHT // 2
fov = math.pi / 3
HALF_FOV = fov / 2
NUM_RAY = 120
dist = NUM_RAY / (2 * math.tan(HALF_FOV))
DELTA_ANGLE = fov / NUM_RAY
PROJ_COEFF = 3 * dist * int(TILE)
SCALE = WIDTH // NUM_RAY
PENTA_HEIGHT = 5 * HEIGHT

CENTER_RAY = NUM_RAY // 2 - 1
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
HALF_TEXTURE_HEIGHT = TEXTURE_HEIGHT // 2
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

@njit(fastmath=True)
def mapping(ox, oy):
    return (ox // TILE) * TILE, (oy // TILE) * TILE

@njit(fastmath=True)
def ray_caster( player_pos, player_angle, world_map, world_width, world_height):

    wall_passed = []
    texture_v, texture_h = 1, 1

    # capture6.png --> 9
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    current_angle = player_angle - HALF_FOV

    for ray in range(NUM_RAY):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + TILE, 1)if cos_a >= 0 else (xm, -1)
        for i in range(0, world_width, TILE):
            depth_v = (x - ox) / cos_a
            y_v = oy + depth_v * sin_a
            tile_v = mapping(x + dx, y_v)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE
            
        # horizontals
        y, dy = (ym + TILE, 1)if sin_a >= 0 else (ym, -1)
        for i in range(0, world_height, TILE):
            depth_h = (y - oy) / sin_a
            x_h = ox + depth_h * cos_a
            tile_h = mapping(x_h, y + dy)
            if tile_h  in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        depth, offset, texture = (depth_v, y_v, texture_v) if depth_v < depth_h else (depth_h, x_h, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - current_angle)
        depth = max(depth, 0.00001)
        proj_height = int(PROJ_COEFF / depth)
        # projection_height = min(int(PROJ_COEFF / depth), PENTA_HEIGHT)
        
        wall_passed.append((depth, offset, proj_height, texture))
        
        current_angle += DELTA_ANGLE

    return wall_passed

def ray_casting_walls(player_pos, player_angle, textures, world_map, world_width, world_height):
    casted_walls = ray_caster(player_pos, player_angle, world_map, world_width, world_height)
    wall_shot = casted_walls[CENTER_RAY][0], casted_walls[CENTER_RAY][2]
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > HEIGHT:
            coeff = proj_height / HEIGHT
            texture_height = TEXTURE_HEIGHT / coeff
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                                       HALF_TEXTURE_HEIGHT - texture_height // 2,
                                                       TEXTURE_SCALE, texture_height)
            wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
            wall_pos = (ray * SCALE, 0)

        else:
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
    return walls, wall_shot












