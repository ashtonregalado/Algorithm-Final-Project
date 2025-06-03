import pygame
from damage import Damage

pygame.init()

def enemyDamageGameplay(enemy, character):
    
    enemy_health = enemy.health

    character_attack = character.attack

    enemy_damage = Damage.damage(character_attack, enemy_health )


    enemy.takeDamage(enemy_damage)


def characterDamageGameplay(character, enemy):
    enemy_attack = enemy.attack
    character_health = character.health

    character_damage = Damage.damage(enemy_attack, character_health)

    character.takeDamage(character_damage)