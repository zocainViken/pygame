import pygame
import random 

from player import Bird
from pipe import Pipe
from button import Button

class Game:
    def __init__(self) -> None:
        # def some basic screen info
        screen_height = 640
        screen_width = 720
        self.screen_height = 640
        self.screen_width = 720
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Flappy Bird')

        # def some global game variable
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        self.color = (255, 255, 255)
        # load some image
        self.bg = pygame.image.load('img/bg.png')
        self.bg = pygame.transform.scale(self.bg, (720, 543))
        self.ground = pygame.image.load('img/ground.png')
        self.restart_button_image = pygame.image.load('img/restart.png')
        # create button
        self.button = Button(self.screen_width // 2 -50, self.screen_height // 2 - 100, self.restart_button_image)
        
        # load some music
        self.die_sound = pygame.mixer.Sound('sound/die.wav')
        self.music = pygame.mixer.Sound('sound/arcade_kid.mp3')
        self.hit_sound = pygame.mixer.Sound('sound/hit.wav')
        self.point_sound = pygame.mixer.Sound('sound/point.wav')
        self.swoosh_sound = pygame.mixer.Sound('sound/swooshing.wav')
        self.wing_sound = pygame.mixer.Sound('sound/wing.wav')
        
        # def some game variable
        self.game_over = False
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.score = 0
        self.pipe_passed = False


        # create our player
        self.flappy = Bird(100, (screen_height / 2), self.swoosh_sound, self.die_sound)

        # create our pipes
        '''self.bottom_pipe = Pipe(screen_width, (screen_height / 2), -1)
        self.top_pipe = Pipe(screen_width, (screen_height / 2), 1)'''
        self.pipe_frequency = 1500# milliseconds
        self.last_pipe = pygame.time.get_ticks()
        
    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.color)
        self.screen.blit(img, (x, y))

    def reset_game(self, pipe_group):
        pipe_group.empty()
        # 100, (screen_height / 2)
        self.flappy.rect.x = 100
        self.flappy.rect.y = (self.screen_height / 2)
        self.score = 0
        score = 0
        return self.score, score

    def run(self):
        # create our bird group
        bird_group = pygame.sprite.Group()
        bird_group.add(self.flappy)

        pipe_group = pygame.sprite.Group()
        
        

        score = 0
        run = True
        
        
        while run:
            # set our fps
            self.clock.tick(self.FPS)
            #self.music.play()

            # draw image onto screen
            self.screen.blit(self.bg, (0, 0))
            
            bird_group.draw(self.screen)
            bird_group.update()# not working ?
            #self.flappy.update()

            
            pipe_group.draw(self.screen)
            #pipe_group.update(self.scroll_speed)
            # check player score
            if len(pipe_group) > 0:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and self.pipe_passed == False:
                    self.pipe_passed = True
                
                if self.pipe_passed == True:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        self.pipe_passed == False
                        score += 1
                        self.point_sound.play()
                    
                    self.score = int(score/20)
                

            self.draw_text(str(self.score), int(self.screen_width / 2), 40)

            # look for collision
            if self.flappy.dead == False:
                if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or self.flappy.rect.top < 0:
                    # game_over = True
                    self.flappy.dead = True
                    self.hit_sound.play()

            if self.flappy.dead == False:
                # generate new pipes
                time_now = pygame.time.get_ticks()
                if time_now - self.last_pipe > self.pipe_frequency and self.flappy.flying == True:
                    # generate random pipe position
                    pipe_height = random.randint(-100, 100)
                    bottom_pipe = Pipe(self.screen_width, (self.screen_height / 2) + pipe_height, -1)
                    top_pipe = Pipe(self.screen_width, (self.screen_height / 2) + pipe_height, 1)
                    pipe_group.add(bottom_pipe)
                    pipe_group.add(top_pipe)
                    self.last_pipe = pygame.time.get_ticks()

                # draw and scroll the ground
                self.screen.blit(self.ground, (self.ground_scroll, 540))
                self.ground_scroll -= self.scroll_speed
                # extend our ground image
                if abs(self.ground_scroll) > 35:
                    self.ground_scroll = 0
                pipe_group.update(self.scroll_speed)

            else:
                self.screen.blit(self.ground, (0, 540))
                

            # check for game over
            if self.flappy.dead == True:
                if self.button.draw(self.screen):
                    self.flappy.dead = False
                    self.score, score = self.reset_game(pipe_group)

            # check if player want to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.flappy.flying == False and self.flappy.dead == False:
                    self.flappy.flying = True


            pygame.display.update()

        pygame.quit()