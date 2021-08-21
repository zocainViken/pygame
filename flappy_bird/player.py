import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, swoosh_sound, die_sound):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.swoosh_sound = swoosh_sound
        self.die_sound = die_sound
        for num in range(1, 5):
            img = pygame.image.load(f'img/bird{num}.png').convert_alpha()
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # add some game variable to our player
        self.vel = 0
        self.clicked = False
        self.flying = False
        # game over
        self.dead = False

    def update_animation(self):
        if self.dead == False:
            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index == len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            # add rotation to the bird
            self.image = pygame.transform.rotate(self.images[self.index], -self.vel*3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -80)

    def update_movement(self):
        # set max gravity 
        if self.flying == True:
            self.vel += 0.5
            if self.vel > 10:
                self.vel = 10
            # if flappy touch ground
            if self.rect.bottom < 540:
                self.rect.y += int(self.vel)
            # if player touch the ground
            if self.rect.bottom >= 540:
                self.dead = True
                self.flying = False
                self.die_sound.play()

        # set jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10
            self.swoosh_sound.play()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
    def update(self):
        self.update_animation()
        self.update_movement()



















