import pygame
from comet import Comet

# creer une classe pour gerer l'evenement de chute de comette
class CometFallEvent():
    # Lors du chargement -> creer un compteur
    def __init__(self, game) -> None:
        self.percent = 0
        self.percent_speed = 30
        self.game = game
        self.fall_mode = False

        # definir un groupe de sprite pour faire tomber plusieur cométe
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed / 100

    def is_full_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0

    def attempt_fall(self):
        # la jauge est complétement charger
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            self.meteor_fall()
            #self.reset_percent()
            self.fall_mode = True # on active l'évémnement

    
    def meteor_fall(self):
        # on veux plusieur cométe à tomber donc on fais une boucle entre 5 et 10
        for i in range(5, 10):
            # faire apparaitre une comet
            self.all_comets.add(Comet(self))

    def update_bar(self, surface):
        # ajouter du pourcentage à la bar
        self.add_percent()

        # le background
        pygame.draw.rect(surface, (0, 0, 0),
                [
                    0,# l'axes des x
                    surface.get_height() - 10 , # l'axes des y
                    surface.get_width(), #  longeur de la fenetre
                    10, #                 eppaisseur de la bar
                ])
        # la bar front
        pygame.draw.rect(surface, ( 92, 32, 213 ),
                [
                    0,# l'axes des x
                    surface.get_height() - 10, # l'axes des y
                    (surface.get_width() / 100) * self.percent, #  longeur de la fenetre
                    10, #                 eppaisseur de la bar
                ]) 

















