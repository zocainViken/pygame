from typing import FrozenSet
import pygame
from pygame.transform import scale 
from drawing import Drawing
import math
import os

tile = 50
num_ray = 120
width = 600
double_pi = 2 * math.pi
center_ray = num_ray // 2 - 1
fov = math.pi / 3
half_fov = fov / 2
DELTA_ANGLE = fov / num_ray
dist = num_ray / (2 * math.tan(half_fov))
projection_coefficient = 3 * dist * int(tile)
SCALE = width // num_ray
HEIGHT = 400
half_height = HEIGHT // 2
FAKE_RAYS = 100

class Sprites:
    def __init__(self) -> None:
        self.frame_index = 0
        self.devil_animation = []
        for file in os.listdir('sprites/devil/base/'):
            self.devil_animation.append(pygame.image.load(f'sprites/devil/base/{file}').convert_alpha())
        
        self.sprite_types = {
                                'barrel' : pygame.image.load('sprites/barrel/anim/0.png').convert_alpha(),
                                'pedestral' : pygame.image.load('sprites/pedestal/base/0.png').convert_alpha(),
                                #'devil': [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range( 8)]
                                #'devil': pygame.image.load(f'sprites/devil/base/0.png').convert_alpha(),
                                'devil': self.devil_animation,
                            }
        
        self.list_objects = [
                                SpriteObject(self.sprite_types['barrel'], True, (9, 3.1), 1.8, 0.4),
                                SpriteObject(self.sprite_types['barrel'], True, (9, 2.1), 1.8, 0.4),
                                
                                SpriteObject(self.sprite_types['pedestral'], True, (8.8, 2.5), 1.6, 0.5),
                                SpriteObject(self.sprite_types['pedestral'], True, (8.8, 5.6), 1.6, 0.5),

                                SpriteObject(self.sprite_types['devil'], False, (9, 4), -0.2, 0.7),
                            ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale) -> None:
        #       ['pedestral'],True, (8.8, 2.5), 1.6, 0.5)
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * tile, pos[1] * tile
        self.shift = shift
        self.scale = scale

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = center_ray + delta_rays
        distance_to_sprite *= math.cos(half_fov - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= num_ray - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            projection_height = min(int(projection_coefficient  / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_projection_height = projection_height // 2
            shift = half_projection_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += double_pi
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - half_projection_height, half_height - half_projection_height + shift)
            sprite = pygame.transform.scale(self.object, (projection_height, projection_height))
            
            return (distance_to_sprite, sprite, sprite_pos)

        else:
            return (False,)











