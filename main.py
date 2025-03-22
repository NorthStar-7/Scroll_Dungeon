import pyxel
import random 

pyxel.init(300, 500, title="Scroll Dungeon")
class Joueur:
    def __init__(self):
        self.xSize = 16
        self.ySize = 16
        self.jump_buffer = 0
        self.x = 300 // 2 - self.xSize // 2  
        self.y = 500 // 2 - self.ySize // 2
        self.vy = 0
        self.surPlateforme = False

    def update(self):
        global score
        
        
        self.surPlateforme, adjust = self.sur_Plateforme()
        
        if self.vy < 8: #Limiter la gravité a 8 pixels par frame
            self.vy += 0.5
            
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.jump_buffer = 5  # Pour améliorer la reactivité du saut, et eviter que on ne saute pas meme quand on appuie sur espace

        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        
        if self.jump_buffer>0 and self.surPlateforme:
            self.vy = -9
            self.surPlateforme = False
            
        elif self.surPlateforme:
            self.vy = 1.5
            self.y = adjust - self.ySize
            
        self.y += self.vy #Modifier la gravité réellement
        
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < 284: #Mouvement left and right
            self.x += 3
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x += -3
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.xSize, self.ySize, 8)
    
    def sur_Plateforme(self): #Cette fonction permet de verifier si le joueur est sur une plateforme, qu'elle soit normale ou cassante. Si il est sur la surface de la plateforme, et il tombe, return True
        for plat in list_plateformes:
            if collision(self, plat, True) and self.vy > 0:
                return True, plat.y
        for platC in list_plateformesCassantes:
            if collision(self, platC, True) and self.vy > 0:
                return True, platC.y
        return False, 0
        
    def toucherEnnemi(self):
        for foe in enemies:
            if collision(self, foe):
                return True
        return False
        

class Plateforme:
    def __init__(self, x, y):
        self.xSize = 80
        self.ySize = 5
        self.x = x
        self.y = y
    
    def update(self): #Faire descendre la plateforme, et la faire respawn en haut si la plateforme arrive tout en bas selon des parametres semi-aléatoires.
        self.y += 2
        if self.y > 500:
            y_min = min(plat.y for plat in list_plateformes if plat.y < 500)  
            self.y = y_min - random.randint(40, 120)
            self.x = random.randint(10, 300 - self.xSize - 10)
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.xSize, self.ySize, 7)
        
class PlateformeCassante:
    def __init__(self, x, y):
        self.xSize = 80
        self.ySize = 5
        self.x = x
        self.y = y
        self.timer = 0
        self.etat = True
    
    def update(self): #Faire descendre la plateforme, et la faire respawn en haut si la plateforme arrive tout en bas selon des parametres semi-aléatoires.
        self.y += 2
        if self.y > 500 or not self.etat:
            y_min = min(plat.y for plat in list_plateformes if plat.y < 500)  
            self.y = y_min - random.randint(40, 120)
            self.x = random.randint(10, 300 - self.xSize - 10)
            self.etat = True
            self.timer = 0
            
        if self.timer == 0 and collision(joueur, self, True) and joueur.vy > 0:
            self.timer = 1
        
        if self.timer > 0:
            self.timer += 1
            if self.timer > 30:
                self.etat = False
            
    def draw(self):
        pyxel.rect(self.x, self.y, self.xSize, self.ySize, 9)
        
class Enemies:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.xSize = 16
        self.ySize = 16

    def update(self):
        self.y += 5
        if self.y > 500:  
            self.y = random.randint(-100, -50)
            self.x = random.randint(10, 300 - self.xSize) 

    def draw(self):
        pyxel.circ(self.x + self.xSize // 2, self.y + self.ySize // 2, self.xSize // 2, 4)
 
def collision(obj1, obj2, plat=False):
    if plat: #Verifie si le joueur est sur la surface de la plateforme
        return (obj1.y + obj1.ySize >= obj2.y and  # Allow slight overlap
                obj1.y + obj1.ySize <= obj2.y + obj2.ySize and  # Still on top surface
                obj1.x + obj1.xSize > obj2.x and 
                obj1.x < obj2.x + obj2.xSize)
    else: #Verifie si il y a un contact quelconque entre les deux objects
        return (obj1.x < obj2.x + obj2.xSize and obj1.x + obj1.xSize > obj2.x and obj1.y < obj2.y + obj2.ySize and obj1.y + obj1.ySize > obj2.y)

joueur = Joueur()
list_plateformes = [Plateforme(random.randint(150, 180), random.randint(100, 500)) for i in range(6)]
list_plateformesCassantes = [PlateformeCassante(random.randint(10, 210), random.randint(100, 400)) for i in range(4)]
enemies = [Enemies(random.randint(10, 300),random.randint(100, 550) ) for _ in range(3)] 
jeu_demarre = False
game_over = False
score = 0


def update():
    global jeu_demarre, game_over, framecount
    
    for plat in list_plateformes:
        plat.update()
        
    for platC in list_plateformesCassantes:
        platC.update()
    
    if not jeu_demarre:
        if pyxel.btnp(pyxel.KEY_SPACE):
            jeu_demarre = True
            joueur.vy = -10
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
    
        for plat in list_plateformes:
            plat.draw()
            
        for platC in list_plateformesCassantes:
            platC.draw()
            
            
    else:
        if joueur.y > 500 or joueur.toucherEnnemi():
            game_over = True
            
        if game_over: 
            pyxel.text(95, 300, "GAME OVER ! Cliquer sur echap", 8) 
            pyxel.text(95, 320, f"Score final: {score}", 7)  
            return
        
        else:
            joueur.draw()
                
            for plat in list_plateformes:
                plat.draw()
                
            for platC in list_plateformesCassantes:
                platC.draw()
                
            for foe in enemies:
                foe.draw()
                
            
pyxel.run(update, draw) 
