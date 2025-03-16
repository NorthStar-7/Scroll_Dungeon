# Scroll_Dungeon
Scroll dungeon project NSI

How things work:
Class for each type of element on the screen, which boils down to:
The player, static(ish) environnemental elements, enemies and eventually powerups
Every single element will move down at a set pace (universall_scroll) to give the illusion of the screen moving up. The player's gravity will be different depending on their actions

player: x and y coordinates, movement will be with arrow keys. when resting, follow universal scroll to match the platforms scroll. 
when jumping, move up at a speed depending on how long ago you jumped (accelerate early, decelerate then stop later), 
then fall down at a speed depending on how long ago you began falling (slow early, then accelerate to max gravity later) until you either die or land on a platform, then you go back to resting.


Environnement class: 
element-type: normal platform
moving platform 
breaking platform (cannot be touched after n time)
cloud platform (cannot be touched)
trap platform (will kill the player if they are on it after n time)
spikes (will kill the player if they are on it at all)
Each element will spawn randomly, with a set quota of platforms and traps being spawned to ensure fairness and difficulty
