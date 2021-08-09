import pygame
from game import Game
import math

pygame.init()

# definition des fps
clock = pygame.time.Clock()
FPS = 60

RUN = True
MAIN_BG = pygame.image.load('assets/assets/bg.jpg')
# on genere la fenetre de notre jeu

#creation de la fenetre de la fenetre
screen = pygame.display.set_mode((800, 600))# creation de la fenetre l = 800px x h = 600px
pygame.display.set_caption('game name')# changer le titre de la fenetre

# on viens charger notre baniere
banner = pygame.image.load('assets/assets/banner.png')
banner = pygame.transform.scale(banner, (380, 340))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)# on arrondie à l'entier suivant
banner_rect.y = math.ceil(screen.get_width() / 6)# on arrondie à l'entier suivant

# on viens importer notre bouton de lancement
play_button = pygame.image.load('assets/assets/button.png')
play_button = pygame.transform.scale(play_button, (300, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)# on arrondie à l'entier suivant
play_button_rect.y = math.ceil(screen.get_width() / 2.3 + 15)# on arrondie à l'entier suivant

# on viens charger notre jeu
game = Game()



while RUN:
    
    # dessiner notre arriere plan sur la surface de de l'écran
    screen.blit(MAIN_BG, (-500, -300))# (largeur, hauteur)

    # verifier si le jeu est lancé ou non
    if game.is_playing:
        # on declenche la partie
        game.update(screen)

    # verifier si notre jeux n'est pas lancer
    else:
        # ajouter ecran d'acceuil
        
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    pygame.display.flip()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # verfification si la souris est en collision avec le bouton jouer
            if play_button_rect.collidepoint(event.pos):
                # on lance le jeux
                game.start()
                # on viens jouer le sons du jeux
                game.sound_manager.play('click')

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # detecter si la touche espace est enclenché
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    # on lance le jeux
                    game.start()
                    # on viens jouer le sons du jeux
                    game.sound_manager.play('click')

    # fixer le nombre de fps avant la fin de la boucle
    clock.tick(FPS)
        





pygame.quit()

            




