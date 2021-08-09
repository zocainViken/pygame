import pygame 

# on vas generer la classe qui vas generer le projectile de notre joueur
class Projectile(pygame.sprite.Sprite):

    # definir le constructeur de notre classe
    def __init__(self, player):
        super().__init__()
        self.velocity = 2
        self.player = player
        self.image = pygame.image.load('assets/assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (40, 33))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 100
        self.rect.y = player.rect.y + 100
        # projectille rotation
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        # rotationner le projectille
        self.angle += 6
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)


    def remove(self):
        self.player.all_projectiles.remove(self)


    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        # verifier si on touche une mommy
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            # on supprime le projectile
            self.remove()
            # infliger des dégat
            monster.damage(self.player.attack)

        # verifier si notre projectile à quitter l'ecran
        if self.rect.x > 650:
            self.remove()
        else:
            pass