import pygame
from pygame import sprite
from pygame.key import name
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
        self.map_layer = map_layer
        self.map = 'world'

        tmx_house_data = pytmx.util_pygame.load_pygame('assets/house1.tmx')

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
        self.pnj_can_talk = False
        self.pnj_1 = Player(pnj_position.x, pnj_position.y)
        self.pnj_1.PNJ = True
        self.pnj_group = pygame.sprite.Group()
        self.map_group.add(self.pnj_1)

        self.pnj_list = []
        for object in tmx_data.objects:
            if object.type == 'pnj_1':
                self.pnj_list.append(pygame.Rect(object.x, object.y, object.width, object.height))


        '''pnj_house_position = tmx_house_data.get_object_by_name('bunny')
        self.pnj_can_talk = False
        self.pnj_2 = Player(pnj_house_position.x, pnj_house_position.y)
        self.pnj_2.PNJ = True
        self.pnj_group = pygame.sprite.Group()
        self.map_group.add(self.pnj_2)

        self.pnj_house_list = []
        for object in tmx_data.objects:
            if object.type == 'bunny':
                self.pnj_house_list.append(pygame.Rect(object.x, object.y, object.width, object.height))'''
        
    def draw_dialogue_panel(self):
        panel_img = pygame.image.load('assets/Icons/panel.png').convert_alpha()
        self.screen.blit(panel_img, (0, 0))
        print('draw panel')

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            #print('up')
            self.player.animate = True
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            #print('down')
            self.player.animate = True
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            #print('left')
            self.player.animate = True
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            #print('right')
            self.player.animate = True
            self.player.move_right()

        elif pressed[pygame.K_t]:
            if self.pnj_can_talk == True:
                self.animate = False
                self.pnj_1.basic_talking()
                self.draw_dialogue_panel()
                # draw dialogue menu
                self.pnj_can_talk = False
                #self.animate = True

    def switch_house(self):
        # load tmx map
        tmx_data = pytmx.util_pygame.load_pygame('assets/house1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        pnj_house_position = tmx_data.get_object_by_name('bunny')
        self.pnj_can_talk = False
        self.pnj_2 = Player(pnj_house_position.x, pnj_house_position.y, name='Demona', scale=0.75)
        self.pnj_2.PNJ = True
        self.pnj_group = pygame.sprite.Group()
        

        self.pnj_house_list = []
        for object in tmx_data.objects:
            if object.type == 'bunny':
                self.pnj_house_list.append(pygame.Rect(object.x, object.y, object.width, object.height))
        

        # draw layer group
        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.map_group.add(self.player)
        self.map_group.add(self.pnj_2)
        

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
        #pygame.draw.rect(self.screen, (255, 0, 0), self.player.feet, 4)
        #pygame.draw.rect(self.screen, (0, 255, 0), self.pnj_1.feet, 4)
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

        # check for collision / global
        for sprite in self.map_group.sprites():
            #print(sprite)
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back_collision()
                self.player.animate = False

    def check_pnj_contact(self):
        if self.player.feet.colliderect(self.pnj_1.rect):
            print('touched')
            self.pnj_can_talk = True
            self.player.move_back_collision()
            self.pnj_1.move_back_collision()
        else:
            self.pnj_can_talk = False
        

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
            self.check_pnj_contact()
            # on doit centrer la camera sur notre joueur
            self.map_group.center(self.player.rect.center)
            pygame.draw.rect(self.screen,(255, 0, 0), self.player.feet)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # check if keyboard is released
                if event.type == pygame.KEYUP:
                    # if a is released
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT :
                        #print('left release')
                        self.player.animate = False

                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT :
                        self.player.animate = False
                        #print('right release')
                    
                    if event.key ==  pygame.K_UP :
                        #print('up release')
                        self.player.animate = False

                    if event.key == pygame.K_DOWN :
                        self.player.animate = False
                        #print('down release')
        
            pygame.display.update()
        
        pygame.quit()




