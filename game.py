import pygame
import random
from character import Character
from enemy import Enemy
from damage import Damage
from gameplay import DamageGameplay

pygame.init()

WIDTH,HEIGTH = 800, 600
grid_size = 30
screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
pygame.display.set_caption("Euclid's Algorithm")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

enemy = Enemy(700, 400, 1001)
character = Character(200, 400, 73)

def main():
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                DamageGameplay(enemy, character)

        character.draw(screen)
        enemy.draw(screen)
 
        pygame.display.flip()

    pygame.quit()

main()