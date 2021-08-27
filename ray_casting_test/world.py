


class World:
    def __init__(self):
        self.tile = 50# need to import it from game
        self.text_map = [
                            'WWWWWWWWWWWW', 
                            'W.W......W.W', 
                            'W..W..W....W', 
                            'WW.....W...W', 
                            'W..WW......W', 
                            'W.....WWW..W', 
                            'WWW........W', 
                            'WWWWWWWWWWWW'
                        ]
        self.world_map = set()# what is function set ?
        
        # mini map setting
        self.mini_map = set()# what is function set ?
        self.map_scale = 5
        self.map_tile = self.tile // self.map_scale
        yellow = (250, 250, 0)
        

        for j, row in enumerate(self.text_map):
            for i, char in enumerate(row):
                if char == 'W':
                    self.world_map.add((i * self.tile, j * self.tile))
                    self.mini_map.add((i * self.map_tile, j * self.map_tile))


class MiniMap:
    def __init__(self) -> None:
        self.world = World()
        self.map_scale = 5
        self.map_tile = self.world.tile // self.map_scale
        yellow = (250, 250, 0)

        self.mini_map = set()
























