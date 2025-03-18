import pygame
from character import Character
from enemy import Enemy
from damage import Damage
from gameplay import DamageGameplay
from bullet import Bullet
from damage_text import DamageText
from adjust_stats import AdjustStats

pygame.init()

WIDTH,HEIGTH = 800, 600
grid_size = 30
screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
pygame.display.set_caption("Euclid's Algorithm")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

enemy = Enemy(700, 400, 1001)
character = Character(200, 400, 73)

bullets = []
damage_texts = []



def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        character_add_button = AdjustStats.addAttackButton(screen)
        character_subtract_button = AdjustStats.subtractAttackButton(screen)
        enemy_add_button = AdjustStats.addHealthButton(screen)
        enemy_subtract_button = AdjustStats.subtractHealthButton(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(character.x + 20, character.y + 10))

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if character_add_button.collidepoint(event.pos):
                    character.attack += 1
                if character_subtract_button.collidepoint(event.pos):
                    character.attack -= 1
                if enemy_add_button.collidepoint(event.pos):
                    enemy.health += 1
                if enemy_subtract_button.collidepoint(event.pos):
                    enemy.health -= 1

        for bullet in bullets:
            bullet.update()


        for bullet in bullets[:]:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                DamageGameplay(enemy, character)
                damage_texts.append(DamageText(enemy.x + 10, enemy.y + -20, Damage.damage(character.attack, enemy.health)))
        
        bullets[:] = [bullet for bullet in bullets if bullet.active]

        for bullet in bullets:
            bullet.draw(screen)

        for dmg in damage_texts[:]:
            dmg.update()
            if dmg.duration <= 0:
                damage_texts.remove(dmg)

        for dmg in damage_texts:
            dmg.draw(screen)

        character.draw(screen)
        enemy.draw(screen)
        


 
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()