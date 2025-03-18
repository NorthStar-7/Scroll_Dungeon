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
            self.vy = -7
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
        

class Plateforme:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 78  

    def update(self):
        self.y += 2.5
        if self.y > 650:
            y_min = min(plat.y for plat in plateformes if plat.y < 650)  
            self.y = y_min - random.randint(40, 80)
            self.x = random.randint(10, 300 - self.largeur - 10)

    def draw(self):
        pyxel.rect(self.x, self.y, self.largeur, 5, 7) 

joueur = Joueur()
plateformes = [Plateforme(random.randint(150, 180), random.randint(100, 550)) for i in range(8)]

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
            joueur.vy = -7.5 
    else:
        joueur.update()
       

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
        if joueur.y > 650:
            game_over = True

        if game_over: 
            pyxel.text(95, 300, "GAME OVER ! Cliquer sur echap", 8) 
            pyxel.text(95, 320, f"Score final: {score}", 7)  
            return
        
        else:
            joueur.draw()
            for plat in plateformes:
                plat.draw()


pyxel.run(update, draw)
