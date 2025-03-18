import pygame
from character import Character
from enemy import Enemy
from damage import Damage

pygame.init()
enemy = Enemy(700, 400, 100)
character = Character(200, 400, 50)
damage = Damage.damage(character.attack, enemy.full_health)
print(damage)
