
from sounds import SoundManager
import pygame
from projectile import Projectile
import animation

class Player(animation.AnimateSprite):
    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 300
        self.max_health = 300
        self.attack = 13
        self.vellocity = 3
        # pour pouvoir lancer plusieur projectile
        self.all_projectiles = pygame.sprite.Group()
        #self.image = pygame.image.load('assets/assets/player.png')
        # pour deplacer notre joueur sur notre surface il est important de récupérer le rectangle de notre image
        self.rect = self.image.get_rect()
        self.rect.x = 300# horizon
        self.rect.y = 400# verticale

    def update_animation(self):
        self.animate()
    
    def damage(self, amount):
        # si on peut subir des dégat
        if self.health - amount > amount:
            #infliger des dégat
            self.health -= amount
        else:
            # si le joueur n'a plus de point de vie
            self.game.game_over()

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (5, 24, 167), [self.rect.x + 40, self.rect.y + 20, self.max_health, 9])# background first
        pygame.draw.rect(surface, (7, 244, 79), [self.rect.x + 40, self.rect.y + 20, self.health, 9])

    def move_right(self):
        # on peut aller à droite seulement s'il n'y à pas de collision
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.vellocity
 
    def move_left(self):
        self.rect.x -= self.vellocity

    def launch_projectile(self):
        # creer une nouvelle instance de la classe projectile
        self.all_projectiles.add(Projectile(self))
        # on demarre l'animation
        self.start_animation()
        # on viens jouer le son
        self.game.sound_manager.play('tir')


