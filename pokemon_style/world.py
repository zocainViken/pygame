import pygame
import pytmx
import pyscroll

class World():
    def __init__(self) -> None:
        # load our tmx file
        # load tmx map
        tmx_data = pytmx.util_pygame.load_pygame('assets/main_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map_layer = map_layer
        self.map = 'world'