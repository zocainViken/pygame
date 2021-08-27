
import pygame
from raycasting import RayCasting

class Drawing():
    def __init__(self, screen) -> None:
        self.screen = screen 
        self.ray_casting = RayCasting(self.screen, int(self.screen.get_height()) / 2)
        self.font = pygame.font.SysFont('Arial', 32, bold = True)
        self.width = self.screen.get_width()

    def background(self):
        blue_sky = (2, 120, 245)
        # draw our sky
        pygame.draw.rect(self.screen, blue_sky, (0, 0, self.width, int(self.screen.get_height()) / 2))
        # draw our floor
        pygame.draw.rect(self.screen, (50, 50, 50), (0, int(self.screen.get_height()) / 2, self.width, int(self.screen.get_height()) / 2))

    def world(self, player_pos, player_angle):
        self.ray_casting.ray_caster(self.screen, player_pos, player_angle)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, (255, 0, 0))
        self.screen.blit(render, (self.width - 65, 5))








