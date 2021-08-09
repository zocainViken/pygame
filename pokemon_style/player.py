import pygame
import os
import random



class Player(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.animate = False
        self.speed = 3
        # handle animation
        self.PNJ = False
        self.animation_list =  []# 0: down, 1:left, 2: up, 3: right,
        # action for select animation in animation list
        self.action = 0# 0: down, 1:left, 2: up, 3: right, 
        self.frame_index = 0
        scale = 1
        # load animation for player
        animations_type = ['down', 'left', 'up', 'right']
        for animation in animations_type:
            temp_list = []
            for file in os.listdir(f'assets/player/{animation}/'):
                #print(file)
                img = pygame.image.load(f'assets/player/{animation}/{file}').convert_alpha()
                img_height = img.get_height()
                img_width = img.get_width()
                img = pygame.transform.scale(img,(img_width * scale, img_height * scale) )
                # remove black background image
                img.set_colorkey([255, 255, 255])
                temp_list.append(img)
            self.animation_list.append(temp_list)

        
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.position = [x, y]
        self.old_position = self.position.copy()

        self.update_pnj_time = pygame.time.get_ticks()
        self.pnj_choice = 6

    def save_location(self): self.old_position = self.position.copy()

    def update_animation(self):
        # define timer animation
        animation_cooldown = 100
        # update image on the current frame index
        self.image = self.animation_list[self.action][self.frame_index]
        # check if animate = True
        if self.animate == True:
            # check if enougth time have passed since last update
            if pygame.time.get_ticks() - self.update_time >= animation_cooldown:
                # go to the next frame
                self.frame_index += 1
                # reset timer 
                self.update_time = pygame.time.get_ticks()

                # check if we get out of list
                if self.frame_index >= len(self.animation_list[self.action]):
                    '''if self.action == 3:# if death stop animation
                        self.frame_index = len(self.animation_list[self.action]) -1
                    else:
                        self.frame_index = 0'''
                    self.frame_index = 0

    def move_right(self):
        # define timer animation
        self.action = 3
        if self.animate == True:
            self.position[0] += self.speed
            self.update_animation()
            self.update_position()

    def move_up(self):
        self.action = 2
        if self.animate == True:
            self.position[1] -= self.speed
            self.update_animation()
            self.update_position()

    def move_left(self):
        self.action = 1
        if self.animate == True:
            self.position[0] -= self.speed
            self.update_animation()
            self.update_position()

    def move_down(self):
        self.action = 0
        if self.animate == True:
            self.position[1] += self.speed
            self.update_animation()
            self.update_position()
            
    def get_image(self, X, Y):# récuperer les coordonée de l'image
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (X, Y, 32, 32))
        return image

    def update_position(self):
        # we get a corner position of our player
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back_collision(self):
        self.position = self.old_position
        #self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    # PNJ Mechanics
    def walk_around(self):
        # cool down for choice for mutlple second not 10/sec
        cooldown = 1000
        self.speed = 1
        # if timer done make new choice
        if pygame.time.get_ticks() - self.update_pnj_time >= cooldown and self.PNJ == True:
            random_choice = random.randrange(0, 6)
            self.pnj_choice = random_choice
            self.update_pnj_time = pygame.time.get_ticks()
        # get choice for movement
        else:
            self.animate = True
            choice = self.pnj_choice
            #choice = self.action
            if choice >= 4:
                print('No movement')
                self.animate = False
                pass
            # 0: down, 1:left, 2: up, 3: right
            elif choice == 0:
                self.animate = True
                self.action = choice
                self.move_down()
                print('move down')
            elif choice == 1:
                self.animate = True
                self.action = choice
                self.move_left()
                print('move left')
            elif choice == 2:
                self.animate = True
                self.action = choice
                self.move_up()
                print('move up')
            elif choice == 4:
                self.animate = True
                self.action = choice
                self.move_right()
                print('move right')

    def basic_talking(self):
        if self.PNJ == True:
            print('I can talk now')









