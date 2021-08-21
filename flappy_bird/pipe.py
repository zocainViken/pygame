import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        self.pipe_gap = 175
        # position 1 = top | position -1 = bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y +  int(self.pipe_gap / 2)]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()








