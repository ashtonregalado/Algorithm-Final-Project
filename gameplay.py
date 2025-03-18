import pygame
import random
from damage import Damage

pygame.init()

def DamageGameplay(enemy, character):
    
    enemy_health = enemy.health
    chracter_attack = character.attack

    damage = Damage.damage(chracter_attack, enemy_health )

    enemy.take_damage(damage)