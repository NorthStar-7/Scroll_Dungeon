import pyxel
import random

pyxel.init(300, 500, title="Scroll Dungeon")

class Player:
    def __init__(self):
        self.taille = 16
        self.x = 300 // 2 - self.taille//2
        self.y = 500 // 2 - self.taille//2
        self.vy = 0 
        self.sur_plateforme = False

    def update_position(self):
        if self.surplateforme and pyxel.btn(KEY_SPACE)
            self.vy = -8

        self.y+=self.vy
        if self.vy<8:
            self.vy += 0.5
    
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < 300-self.taille:
            self.x += 3
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x += -3

        
   '''     
class Environnement:
    def __init__(self, x, y, size, element_type):
        self.x = x
        self.y = y
        self.size = size
        self.element = element_type
        self.spawntime = pyxel.frame_count
        self.activated = False #For trap objects
'''
