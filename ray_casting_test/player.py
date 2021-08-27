import pygame
import math 


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.angle = 0
        self.speed = 2



    def movement(self):
        # capture1.png
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            #self.y -= self.speed
            self.x += self.speed * cos_a
            self.y += self.speed * sin_a
            #print('W')

        elif keys[pygame.K_s]:
            #self.y += self.speed
            self.x -= self.speed * cos_a
            self.y -= self.speed * sin_a
            #print('S')

        elif keys[pygame.K_a]:
            #self.x -= self.speed
            self.x += self.speed * cos_a
            self.y -= self.speed * sin_a
            #print('A')

        elif keys[pygame.K_d]:
            #self.x += self.speed
            self.x -= self.speed * cos_a
            self.y += self.speed * sin_a
            #print('D')

        elif keys[pygame.K_LEFT]:
            self.angle -= 0.04

        elif keys[pygame.K_RIGHT]:
            self.angle += 0.04
        
        self.pos = (self.x, self.y)














































