import pyxel
import random

pyxel.init(300, 500, title="Scroll Dungeon")

class Player:
    def __init__(self):
        self.size = 20
        self.x = 150
        self.y = 150
        self.vy = 0
        self.action = "resting" 
        '''resting, jumping or falling as a string  will determine the player's vertical movement'''
        self.alive = True

    def update_position(self):

        #To do; check if the player is resting on any platform by going through the list of platforms; put the action as resting if anything is true. 
        
        if self.action[0] == "resting":
            self.vy = -1
            if pyxel.btn(KEY_UP): #Jumping when at rest will change the action and falling value
                self.action = "jumping"
                self.vy = 6

        if self.action[0] == "jumping": #What to do with the falling value when jumping
            if self.vy < 0:
                self.vy -= 1
            else:
                self.action = "falling"
            
        if self.action[0] == "falling":
            if self.vy > 5:
                self.vy -= 1

        self.y += self.vy #After all actions and calculations have been made, actually change the y value.
        
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

