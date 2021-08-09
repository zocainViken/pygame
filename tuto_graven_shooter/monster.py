import pygame
import random
import animation

class Monster(animation.AnimateSprite):
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        #self.name = name
        #self.size = size
        self.loot_amount = 10
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.1
        self.rect = self.image.get_rect()
        self.rect.x = 710 - random.randint(0, 200)# horizon  - position aleatoi sur 50px 
        self.rect.y = 438 - offset # verticale
        self.start_animation()

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, 3)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def damage(self, amount):
        #infliger des dégat
        self.health -= amount
        # si le monstre est mort
        if self.health <= 0:
            # respawn our monster
            self.rect.x = 710 - random.randint(0, 200)
            self.velocity = random.randint(1, self.default_speed)
            self.health = self.max_health
            # on ajoute des points à notre joueur
            #self.game.score += 20
            self.game.add_score(self.loot_amount)

            # on vérifie si la bar de chute de cométe est chargé au max
            if self.game.comet_event.is_full_loaded:
                # on supprime le monstre
                self.game.all_monsters.remove(self)
                # appel de chute de cométe
                self.game.comet_event.attempt_fall()

    def forward(self):
        # on peut se deplacer uniquement s'il n'y à pas de colliqion avec un joueur( groupe de 1 joueur)
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity

        # si le monstre est encollision avec le joueur
        else:
            # on inflige des défat au joueur
            self.game.player.damage(self.attack)

    def update_health_bar(self, surface):
        # definir une couleur pour l'arriere plan de la jauge gris foncé
        #bar_background_color = (5, 24, 167)

        #definir la position de notre jauge de vie 
        # sa largeur, son épaisseur
        #bar_position = [self.rect.x + 13, self.rect.y - 13, self.health, 5] #[x, y, w, h]
        # definir la position du background
        #bar_background_position = [self.rect.x + 13, self.rect.y - 13, self.max_health, 5]
        
        # dessiner notre barre de vie
        pygame.draw.rect(surface, (5, 24, 167), [self.rect.x + 13, self.rect.y - 13, self.max_health, 5])# background first
        pygame.draw.rect(surface, (7, 244, 79), [self.rect.x + 13, self.rect.y - 13, self.health, 5])

    def update_animation(self):
        self.animate(loop = True)


class Mummy(Monster):
    def __init__(self, game):
        super().__init__(game, 'mummy', (130, 130))
        self.set_speed(3)


class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, 'alien', (250, 250), 100)
        self.health = 250
        self.max_health = 250
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(100)









