import pyxel
import random

pyxel.init(300, 650, title="Scroll Dungeon")



class Joueur:
    def __init__(self):
        self.taille = 16
        self.x = 300 // 2 - self.taille // 2  
        self.y = 650 // 2 - self.taille // 2  
        self.vy = 0
        self.sur_platefore = False

    def update(self):
        self.vy += 0.5  # "gravite"
        self.y += self.vy

        if pyxel.btnp(pyxel.KEY_SPACE) and (self.sur_platefore or self.y >= 634):  
            self.vy = -10
            self.sur_platefore = False 

        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < 284:
            self.x += 3
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x += -3
        
        if self.sur_plateforme() and not self.sur_platefore:  
            global score
            score += 1
        
        self.sur_platefore = self.sur_plateforme() 

    def draw(self):
        pyxel.rect(self.x, self.y, self.taille, self.taille, 8)
    
    def sur_plateforme(self):
        for plat in plateformes:
            if (
                self.x + self.taille > plat.x
                and self.x < plat.x + plat.largeur
                and self.y + self.taille + self.vy > plat.y 
                and self.y + self.taille < plat.y + 5 + self.vy 
            ):
                if self.vy>0:
                    self.y = plat.y - self.taille
                return True
        return False
    
    def contre_ennemi(self):
        for foe in enemies:
            if (
                self.x + self.taille > foe.x
                and self.x < foe.x + foe.taille
                and self.y + self.taille + self.vy > foe.y 
                and self.y + self.taille < foe.y + 5 + self.vy 
            ):
                if self.vy>0:
                    self.y = foe.y - self.taille
                return True
        return False     

class Plateforme:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 78  

    def update(self):
        self.y += 4
        if self.y > 650:
            y_min = min(plat.y for plat in plateformes if plat.y < 650)  
            self.y = y_min - random.randint(40, 80)
            self.x = random.randint(10, 300 - self.largeur - 10)

    def draw(self):
        pyxel.rect(self.x, self.y, self.largeur, 5, 7)
        
class Enemies:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.taille = 16
        self.vitesse_descente = 5

    def update(self):
        self.y += self.vitesse_descente
        if self.y > 650:  
            self.y = random.randint(-100, -50)
            self.x = random.randint(10, 300 - self.taille) 

    def draw(self):
        pyxel.circ(self.x + self.taille // 2, self.y + self.taille // 2, self.taille // 2, 9)

#variables pour initialiser les elements
joueur = Joueur()
plateformes = [Plateforme(random.randint(150, 180), random.randint(100, 550)) for i in range(8)]
enemies = [Enemies(random.randint(10, 300),random.randint(100, 550) ) for _ in range(3)] 
# variables pour gérer l'état du jeu
jeu_demarre = False
game_over = False
score = 0


def update():
    global jeu_demarre, game_over

    for plat in plateformes:
        plat.update()

    if not jeu_demarre:
        if pyxel.btnp(pyxel.KEY_SPACE):
            jeu_demarre = True
            joueur.vy = -8 
    else:
        joueur.update()
        for foe in enemies:
            foe.update()

def draw():
    global game_over
    pyxel.cls(0) 
    
    
    pyxel.text(5, 5, f"Score: {score}", 7)
    
    if not jeu_demarre:
        pyxel.text(120, 300, "Appuyez sur Espace", 7) 
        joueur.draw()
        for plat in plateformes:
            plat.draw()  

    else:
        if joueur.y > 650 or joueur.contre_ennemi() == True:
            game_over = True

        if game_over: 
            pyxel.text(95, 300, "GAME OVER ! Cliquer sur echap", 8) 
            pyxel.text(95, 320, f"Score final: {score}", 7)  
            return
        
        else:
            joueur.draw()
            for foe in enemies:
                foe.draw()
            for plat in plateformes:
                plat.draw()


pyxel.run(update, draw)
