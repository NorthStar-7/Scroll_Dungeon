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
        self.vitesse = 3

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

    def contre_ennemi(self):
        for foe in enemies:
            if (
                self.x + self.taille > foe.x
                and self.x < foe.x + foe.taille
                and self.y + self.taille > foe.y 
                and self.y < foe.y + foe.taille
            ):
                return True
        return False 

    def attrape_perk(self):
        global score
        for perk in perks:
            if (
                self.x + self.taille > perk.x
                and self.x < perk.x + perk.taille
                and self.y + self.taille > perk.y 
                and self.y < perk.y + perk.taille
            ):
                if perk.type == "jump":
                    self.vy = -12  # Augmente le saut
                elif perk.type == "speed":
                    self.vitesse = 5  # Augmente la vitesse
                elif perk.type == "score":
                    score += 5  # Ajoute du score
                perk.reset()
        
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
        pyxel.rect(self.x, self.y, self.taille, self.taille, 10)

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

