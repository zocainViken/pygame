
import pygame



class Button():
    def __init__(self, x, y, image) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse over button
        if self.rect.collidepoint(pos):
            # check if we click on it
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
            

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

















