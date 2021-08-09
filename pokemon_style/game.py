import pygame
from pygame import sprite
import pytmx
import pyscroll
from player import Player


class Game:
    def __init__(self) -> None:    
        # create game screen
        WIDTH = 800
        HEIGHT = 400
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.name = pygame.display.set_caption('pygamon / test')

        # load tmx map
        tmx_data = pytmx.util_pygame.load_pygame('assets/main_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map = 'world'

        # we create our player
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x, player_position.y)

        # draw layer group
        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.map_group.add(self.player)
        

        # collision group
        self.walls = []
        for object in tmx_data.objects:
            if object.type == 'collision':
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # check collision rect for enter in house
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        
        # create our pnj
        pnj_position = tmx_data.get_object_by_name('pnj_1')
        self.pnj_1 = Player(pnj_position.x, pnj_position.y)
        self.pnj_1.PNJ = True
        self.pnj_group = pygame.sprite.Group()
        self.map_group.add(self.pnj_1)

        self.pnj_list = []
        for object in tmx_data.objects:
            if object.type == 'pnj_1':
                self.pnj_list.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # check for colision with pnj / dialogue
        pnj_quest = tmx_data.get_object_by_name('pnj_1')
        self.pnj_quest_rect_rect = pygame.Rect(pnj_quest.x, pnj_quest.y, pnj_quest.width, pnj_quest.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            print('up')
            self.player.animate = True
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            print('down')
            self.player.animate = True
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            print('left')
            self.player.animate = True
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            print('right')
            self.player.animate = True
            self.player.move_right()

    def switch_house(self):
        # load tmx map
        tmx_data = pytmx.util_pygame.load_pygame('assets/house1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # draw layer group
        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.map_group.add(self.player)

        # collision group
        self.walls = []
        for object in tmx_data.objects:
            if object.type == 'collision':
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # check collision rect for enter in house
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # get spawn position in house
        house_spawn_point = tmx_data.get_object_by_name('spawn_house1')
        self.player.position[0] = house_spawn_point.x
        self.player.position[1] = house_spawn_point.y - 20

    def switch_world(self):
        # load tmx map
        tmx_data = pytmx.util_pygame.load_pygame('assets/main_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # draw layer group
        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.map_group.add(self.player)

        # collision group
        self.walls = []
        for object in tmx_data.objects:
            if object.type == 'collision':
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # check collision rect for exit house
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        # get spawn position un house
        house_spawn_point = tmx_data.get_object_by_name('spawn_house_exit1')
        self.player.position[0] = house_spawn_point.x
        self.player.position[1] = house_spawn_point.y - 20

    def dialogue(self):
        # if player touch pnj
        tmx_data = pytmx.util_pygame.load_pygame('assets/main_map.tmx')
        enter_house = tmx_data.get_object_by_name('pnj_1')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)       

    def update(self):
        self.pnj_1.walk_around()
        
        self.map_group.update()
        # check for collision / house
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'
        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'
            self.map_group.add(self.pnj_1)

        # check for collision / pnj / quest
        

        # check for collision / global
        for sprite in self.map_group.sprites():
            #print(sprite)
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back_collision()
                self.player.animate = False

    def run(self):
                
        # define fps
        clock = pygame.time.Clock()
        FPS = 30
        # start game loop
        running = True

        while running:
            
            self.player.save_location()
            self.pnj_1.save_location()
            self.handle_input()
            clock.tick(FPS)
            self.map_group.draw(self.screen)
            self.update()
            # on doit centrer la camera sur notre joueur
            self.map_group.center(self.player.rect.center)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # check if keyboard is released
                if event.type == pygame.KEYUP:
                    # if a is released
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT :
                        #action = self.player.action
                        #self.player.idle(action)
                        print('left release')
                        self.player.animate = False

                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT :
                        self.player.animate = False
                        print('right release')
                    
                    if event.key ==  pygame.K_UP :
                        print('up release')
                        self.player.animate = False

                    if event.key == pygame.K_DOWN :
                        self.player.animate = False
                        print('down release')
        
            pygame.display.update()
        
        pygame.quit()




