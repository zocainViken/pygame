


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

        for j, row in enumerate(self.text_map):
            for i, char in enumerate(row):
                if char == 'W':
                    self.world_map.add((i * self.tile, j * self.tile))



























