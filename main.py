import pyxel
import random

pyxel.init(300, 500, title="Scroll Dungeon")

class Joueur:
    def __init__(self):
        self.taille = 16
        self.x = 300 // 2 - self.taille // 2  
        self.y = 650 // 2 - self.taille // 2  
        self.vy = 0
        self.vitesse_x = 3
        self.jump_force = -10
        self.sur_platefore = False
        self.score_multiplier = 1

    def mettre_a_jour(self):
        self.vy += 0.5  # Gravité
        self.y += self.vy

        if pyxel.btnp(pyxel.KEY_SPACE) and (self.sur_platefore or self.y >= 634):  
            self.vy = self.jump_force
            self.sur_platefore = False 

        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < 284:
            self.x += self.vitesse_x
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= self.vitesse_x
        
        if self.sur_plateforme() and not self.sur_platefore:  
            global score
            score += 1 * self.score_multiplier
        
        self.sur_platefore = self.sur_plateforme() 
    
    def dessiner(self):
        pyxel.rect(self.x, self.y, self.taille, self.taille, 8)
    
    def sur_plateforme(self):
        for plat in plateformes:
            if (
                self.x + self.taille > plat.x
                and self.x < plat.x + plat.largeur
                and self.y + self.taille + self.vy > plat.y 
                and self.y + self.taille < plat.y + 5 + self.vy 
            ):
                if self.vy > 0:
                    self.y = plat.y - self.taille
                return True
        return False
    
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
    
    def ramasse_perk(self):
        for perk in perks:
            if (
                self.x + self.taille > perk.x
                and self.x < perk.x + perk.taille
                and self.y + self.taille > perk.y 
                and self.y < perk.y + perk.taille
            ):
                if perk.type == "jump":
                    self.jump_force = -20
                elif perk.type == "speed":
                    self.vitesse_x = 6
                elif perk.type == "score":
                    self.score_multiplier = 2
                perks.remove(perk)

class Plateforme:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largeur = 78  

    def mettre_a_jour(self):
        self.y += 4
        if self.y > 650:
            y_min = min(plat.y for plat in plateformes if plat.y < 650)  
            self.y = y_min - random.randint(40, 80)
            self.x = random.randint(10, 300 - self.largeur - 10)

    def dessiner(self):
        pyxel.rect(self.x, self.y, self.largeur, 5, 7)

class Enemi:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.taille = 16
        self.vitesse_descente = 5

    def mettre_a_jour(self):
        self.y += self.vitesse_descente
        if self.y > 650:  
            self.y = random.randint(-100, -50)
            self.x = random.randint(10, 300 - self.taille) 

    def dessiner(self):
        pyxel.rect(self.x, self.y, self.taille, self.taille, 9)

class Perk:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.taille = 12
        self.vitesse_descente = 3
        self.type = type
        self.couleur = {"jump": 12, "speed": 11, "score": 10}[type]

    def mettre_a_jour(self):
        self.y += self.vitesse_descente
        if self.y > 650:  
            self.y = random.randint(-100, -50)
            self.x = random.randint(10, 300 - self.taille) 

    def dessiner(self):
        pyxel.circ(self.x + self.taille // 2, self.y + self.taille // 2, self.taille // 2, self.couleur)

# Variables pour initialiser les éléments
joueur = Joueur()
plateformes = [Plateforme(random.randint(150, 180), random.randint(100, 550)) for _ in range(8)]
enemies = [Enemi(random.randint(10, 300), random.randint(100, 550)) for _ in range(3)]
perks = [Perk(random.randint(10, 300), random.randint(-500, -50), random.choice(["jump", "speed", "score"])) for _ in range(6)]

# Variables pour gérer l'état du jeu
jeu_demarre = False
game_over = False
score = 0

def mettre_a_jour():
    global jeu_demarre, game_over

    for plat in plateformes:
        plat.mettre_a_jour()

    if not jeu_demarre:
        if pyxel.btnp(pyxel.KEY_SPACE):
            jeu_demarre = True
            joueur.vy = -8 
    else:
        joueur.mettre_a_jour()
        joueur.ramasse_perk()
        for foe in enemies:
            foe.mettre_a_jour()
        for perk in perks:
            perk.mettre_a_jour()

def dessiner():
    global game_over
    pyxel.cls(0) 
    pyxel.text(5, 5, f"Score: {score}", 7)
    
    if not jeu_demarre:
        pyxel.text(120, 300, "Appuyez sur Espace", 7) 
        joueur.dessiner()
        for plat in plateformes:
            plat.dessiner()  
    else:
        if joueur.y > 650 or joueur.contre_ennemi():
            game_over = True

        if game_over: 
            pyxel.text(95, 300, "GAME OVER ! Cliquer sur Echap", 8) 
            pyxel.text(95, 320, f"Score final: {score}", 7)  
            return
        else:
            joueur.dessiner()
            for foe in enemies:
                foe.dessiner()
            for perk in perks:
                perk.dessiner()
            for plat in plateformes:
                plat.dessiner()

pyxel.run(mettre_a_jour, dessiner)
