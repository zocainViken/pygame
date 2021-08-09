import pygame
import random

class Comet(pygame.sprite.Sprite):
    
    def __init__(self, comet_event):
        super().__init__()
        # definir l'image de la cométe
        self.image = pygame.image.load('assets/assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 2)
        self.rect.x = random.randint(20, 580)
        self.rect.y = - random.randint(50, 100)
        self.comet_event = comet_event

    def remove(self):
        self.comet_event.all_comets.remove(self)
        # jouer le son de la cométe
        self.comet_event.game.sound_manager.play('meteorite')
        # verifier si le nombre de cométe est de 0
        if len(self.comet_event.all_comets) == 0:
            # remettre la bar à 0
            self.comet_event.reset_percent()
            # faire appaire nos 2 monstres
            self.comet_event.game.start()

    def fall(self):
        self.rect.y += self.velocity

        # ne tombe pas sur le sol
        if self.rect.y >= 500:
            # retirer la cométe
            self.remove()

            # s'il n'y à plus de boule de feu
            if len(self.comet_event.all_comets) == 0:
                #print('l\' fin de la chute de cométe ')
                # remetre notre jauge à 0
                self.comet_event.reset_percent()
                #print(' pluie de meteore')
                self.comet_event.fall_mode = False

        # verifier si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            #print('joueur touché')
            # retirer la boule de feu
            self.remove()
            # faire subir 20 point de degat
            self.comet_event.game.player.damage(20)
            






