
import pygame
from player import Player
from monster import Alien, Monster, Mummy
from comet_event import CometFallEvent
from sounds import SoundManager

class Game:
    def __init__(self):
        # est-ce que le jeu est lancer ou non ?
        self.is_playing = False
        # generer notre joueur
        # groupe de sprite de joueur ? 
        self.all_players = pygame.sprite.Group()# groupe de sprite vierge
        self.player = Player(self)
        self.all_players.add(self.player)
        # generer un manageur de chute de comette
        self.comet_event = CometFallEvent(self)
        # on met le score à 0
        self.score = 0

        # on viens gerer le son
        self.sound_manager = SoundManager()
        
        # charger notre police custom
        self.font = pygame.font.Font('Dancing_Script/static/DancingScript-Bold.ttf', 50)

        # groupe de monstre
        self.all_monsters = pygame.sprite.Group()# groupe de sprite vierge
        # on enregistre les touche active par le joueur
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def add_score(self, point=10):
        self.score += point

    def game_over(self):
        # retirer les monstres, remettre les point de vie du joueur, et mettre le jeu en pause
        # retirer les monstre
        self.all_monsters = pygame.sprite.Group()
        #retirer les cometes
        self.comet_event.all_comets = pygame.sprite.Group()
        # restaurer la bar de chargement
        self.comet_event.reset_percent()
        # remettre les points de vie du joueur
        self.player.health = self.player.max_health
        # remettre le jeu en pause
        self.is_playing = False
        # on remet le score à zero 
        self.score = 0
        # on viens jouer le son
        self.sound_manager.play('game_over')

    def update(self, screen):

        score_text = self.font.render(f'Score: {self.score}', 1, (0, 0, 0))
        # on inject sur la fenetre
        screen.blit(score_text, (20, 20))
        
        # récuperer l'animation du joueur
        self.player.update_animation()
        # appliquer l'image de notre joueur
        screen.blit(self.player.image, self.player.rect)# (largeur, hauteur)
        # actualiser la bar de vie du joueur
        self.player.update_health_bar(screen)

        self.comet_event.update_bar(screen)


        # recuperer les projectille du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()
        # appliquer l'ensemble des images de nos projectiles
        self.player.all_projectiles.draw(screen)

        # recuperer les comets de notre jeux
        for comet in self.comet_event.all_comets:
            comet.fall()
        # appliquer l'ensemble des images de nos comets
        self.comet_event.all_comets.draw(screen)



        # recuperer les monstre de notre jeux
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()
        # appliquer l'image du monstre
        self.all_monsters.draw(screen)

         # verifier si le joueur souhaite aller à droite ou à gauche
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width() +  75:
            self.player.move_right()
        
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -75:
            self.player.move_left()

    def spawn_monster(self, monster_classe_name):
        self.all_monsters.add(monster_classe_name.__call__(self))# call permet d'instancier l'objet

    def check_collision(self, sprite, group):
        return pygame.sprite .spritecollide(sprite, group, False, pygame.sprite.collide_mask)

