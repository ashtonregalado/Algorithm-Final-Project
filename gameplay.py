import pygame
from damage import Damage

pygame.init()

def EnemyDamageGameplay(enemy, character):
    
    enemy_health = enemy.health

    character_attack = character.attack

    enemy_damage = Damage.damage(character_attack, enemy_health )


    enemy.take_damage(enemy_damage)


def CharacterDamageGameplay(character, enemy):
    enemy_attack = enemy.attack
    character_health = character.health

    character_damage = Damage.damage(enemy_attack, character_health)

    character.take_damage(character_damage)