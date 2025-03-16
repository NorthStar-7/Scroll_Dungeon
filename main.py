import pyxel
import random

pyxel.init(300, 500, title="Scroll Dungeon")

class Player:
    def __init__(self):
        self.x = 150
        self.y = 150
        self.action = ["resting", 0] #
        '''resting, jumping or falling as a string  will determine the player's vertical movement
        the number is the action timer (amount of frames player has jumped or fell) to deal with jumping or falling speed
        '''
        self.surplateforme = False #will immediatly put the action at resting when True
        self.alive = True
        
class Environnement:
    def __init__(self, x, y, element_type):
        self.x = x
        self.y = y
        self.element = element_type
        self.spawntime = pyxel.frame_count
        self.activated = False #For trap objects
