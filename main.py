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
        
class Plateforme:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 78  

    def update(self):
        self.y += 2.5  # Vitesse de descente de la plateforme
        if self.y > 650:
            y_min = min(plat.y for plat in plateformes if plat.y < 650)  
            self.y = y_min - random.randint(40, 80)
            self.x = random.randint(10, 300 - self.largeur - 10)

    def draw(self):
        pyxel.rect(self.x, self.y, self.largeur, 5, 7) 

class Enemies:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(-100, -50)
        self.taille = 16
        self.vitesse_descente = 5

    def update(self):
        self.y += self.vitesse_descente
        if self.y > 650:
            self.y = random.randint(-100, -50)
            self.x = random.randint(10, 300 - self.taille) 

    def draw(self):
        pyxel.circ(self.x + self.taille // 2, self.y + self.taille // 2, self.taille // 2, 9)

    def verifier_collision(self, joueur):
        collision_en_x = (self.x < joueur.x + joueur.size) and (self.x + self.taille > joueur.x)
        collision_en_y = (self.y < joueur.y + joueur.size) and (self.y + self.taille > joueur.y)

        return collision_en_x and collision_en_y

class Perk:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.taille = 12
        self.type = type_
        self.vitesse_descente = 2
        self.couleur = {"jump": 12, "speed": 11, "score": 14}[type_]

    def update(self):
        self.y += self.vitesse_descente
        if self.y > 500:
            self.reset()

    def reset(self):
        self.y = random.randint(-150, -50)
        self.x = random.randint(10, 300 - self.taille)
    
    def draw(self):
        pyxel.circ(self.x + self.taille // 2, self.y + self.taille // 2, self.taille // 2, self.couleur)


# Initialisation du joueur et des plateformes
joueur = Joueur()
plateformes = [Plateforme(random.randint(10, 220), random.randint(100, 550)) for _ in range(8)]
enemies = [Enemies(random.randint(10, 300)) for _ in range(3)] 
perks = [Perk(random.randint(10, 300), random.randint(-200, -50), random.choice(["jump", "speed", "score"])) for _ in range(2)]

