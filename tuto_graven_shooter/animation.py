import pygame



class AnimateSprite(pygame.sprite.Sprite):
    # definir les chose à faire à la création
    def __init__(self, sprite_name, size=(200, 200)) -> None:
        super().__init__()
        self.size = size
        self.image = pygame.image.load(f'assets/assets/{sprite_name}.png')
        self.image = pygame.transform.scale(self.image, size)
        self.current_image = 0# on commence l'animation à l'image 0
        self.images = animations.get(sprite_name)   
        self.animation = False 

    # definir une méthode pour démarrer notre animation
    def start_animation(self):
        self.animation = True

    # definir une méthode pour animer notre sprite
    def animate(self, loop=False):
        # on vérifie si notre animation est activé
        if self.animation:
            # passer à l'image suivante
            self.current_image += 1
            # verifier si l'on à atteind la fin de l'animation
            if self.current_image >= len(self.images):
                # on remet l'animation à 0
                self.current_image = 0
                # on verifie que l'on ne soit pas en mode True
                if loop is False:
                    # desactivation de l'animation
                    self.animation = False

            # modifier l'image par la suivante
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)

# definir une fonction pour charger les image d'un sprite
def load_animation_images(sprite_name):
    # on viens charger les 24 images correspondante dans le dossier
    images = []
    # récuperer le chemin
    path = f'assets/assets/{sprite_name}/{sprite_name}'
    #boucler sur chaque image dans le dossier
    for num in range(1, 24):
        image_path = path + str(num) + '.png'
        pygame.image.load(image_path)
        images.append(pygame.image.load(image_path))
    # on renvois le contenu de la liste
    return images

# on vas définir un dictionnaire qui vas contenir les image chargé de chaque sprite
animations = {
                'mummy' : load_animation_images('mummy'),
                'player' : load_animation_images('player'),
                'alien' : load_animation_images('alien'),
            }




