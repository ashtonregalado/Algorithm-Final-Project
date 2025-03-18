import pygame
import random
from damage import Damage

pygame.init()

def DamageGameplay(enemy, character):
    
    enemy_health = enemy.health
    character_attack = character.attack

    damage = Damage.damage(character_attack, enemy_health )

    enemy.take_damage(damage)