

import pygame
import math
from numba import njit

from raycasting import mapping



TILE = 50
fov = math.pi / 3
HALF_FOV = fov / 2
NUM_RAY = 120
dist = NUM_RAY / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * dist * int(TILE)
DELTA_ANGLE = fov / NUM_RAY


@njit(fastmath=True, cache = True)
def ray_casting_player(npc_x, npc_y, blocked_door, world_map, player_x, player_y):
    ox, oy = player_x, player_y
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    current_angle = math.atan2(delta_y, delta_x)
    current_angle += math.pi


    sin_a = math.sin(current_angle)
    cos_a = math.cos(current_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1)if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)), TILE):
        depth_v = (x - ox) / cos_a
        y_v = oy + depth_v * sin_a
        tile_v = mapping(x + dx, y_v)
        if tile_v in world_map or tile_v in blocked_door:
            return False
        x += dx * TILE
        
    # horizontals
    y, dy = (ym + TILE, 1)if sin_a >= 0 else (ym, -1)
    for i in range(0,  int(abs(delta_y)), TILE):
        depth_h = (y - oy) / sin_a
        x_h = ox + depth_h * cos_a
        tile_h = mapping(x_h, y + dy)
        if tile_h  in world_map or tile_h in blocked_door:
            return False
        y += dy * TILE

    return True


class Interaction:
    def __init__(self, player, sprite, drawing, world_map) -> None:
        self.player = player
        self.sprites = sprite
        self.drawing = drawing
        self.world_map = world_map
        self.pain_sound = pygame.mixer.Sound('sound/pain.wav')

    def interaction_object(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_player(obj.x, obj.y, self.sprites.blocked_doors, self.world_map, self.player.x, self.player.y):
                            if obj.flag =='npc':
                                self.pain_sound.play()
                            obj.is_dead = True
                            obj.blocked = None
                            self.drawing.shot_animation_trigger = False
                    
                    if obj.flag in {'door-h', 'door_v'} and obj.distance_to_sprite < TILE:
                        obj.door_open_trigger = True
                        obj.Blocked = False
                    break

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_player(obj.x, obj.y, self.sprites.blocked_doors, self.world_map, self.player.x, self.player.y):
                    obj.npc_action_trigger = True
                    self.npc_movement(obj)
                else:
                    self.npc_action_trigger = False

    def npc_movement(self, obj):
        if obj.distance_to_sprite > TILE:# enemy track me
            if obj.flag == 'npc':
                dx = obj.x - self.player.x
                dy = obj.y - self.player.y

                obj.x = obj.x +1 if dx < 0 else obj.x -1
                obj.y = obj.y +1 if dy < 0 else obj.y -1

    def clear_world(self):
        delete_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove() for obj in delete_objects if obj.delete]

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.mp3')
        pygame.mixer.music.play(10)

    def check_win(self):
        if not len([obj for obj in self.sprites.list_of_object if obj.flag == 'npc' and not obj.is_dead]):
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/win.mp3')
            pygame.mixer.play()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                
                self.drawing.win()












