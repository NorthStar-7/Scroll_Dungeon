import pyxel
import random

pyxel.init(300, 500, title="Scroll Dungeon")

class Player:
    def __init__(self):
        self.size = 20
        self.x = 150
        self.y = 150
        self.action = ["resting", 0] #
        '''resting, jumping or falling as a string  will determine the player's vertical movement
        the number is the action timer (amount of frames player has jumped or fell) to deal with jumping or falling speed
        '''
        self.surplateforme = False #will immediatly put the action at resting when True
        self.alive = True

    def update_position(self):
        if self.action[0] == "resting":
            universal_scroll(self)

        elif self.action[0] == "falling":
            self.y -= 3

        elif self.action[0] == "jumping":
            self.y += 3
            
        if pyxel.btn(KEY_RIGHT) and self.x < 300 - self.size:
            self.x += 2

        if pyxel.btn(KEY_LEFT) and self.x > 0:
            self.x -= 2
        
class Environnement:
    def __init__(self, x, y, size, element_type):
        self.x = x
        self.y = y
        self.size = size
        self.element = element_type
        self.spawntime = pyxel.frame_count
        self.activated = False #For trap objects

def universal_scroll(object):
    self.y -= 1

