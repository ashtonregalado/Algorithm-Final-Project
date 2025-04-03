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
    target_x, target_y = character.x, character.y

    while running:
        screen.fill(WHITE)

        character_add_button = AdjustStats.addAttackButton(screen)
        character_subtract_button = AdjustStats.subtractAttackButton(screen)
        enemy_add_button = AdjustStats.addHealthButton(screen)
        enemy_subtract_button = AdjustStats.subtractHealthButton(screen)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN :
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
                    
                elif not (character_add_button.collidepoint(event.pos) or 
                          character_subtract_button.collidepoint(event.pos) or 
                          enemy_add_button.collidepoint(event.pos) or 
                          enemy_subtract_button.collidepoint(event.pos)):
                    bullets.append(Bullet(character.x + 20, character.y + 10))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            target_x -= character.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            target_x += character.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            target_y -= character.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            target_y += character.speed


        for bullet in bullets:
            bullet.update()

        if enemy.alive:
            for bullet in bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    DamageGameplay(enemy, character)
                    if enemy.alive:
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

        character.move(target_x, target_y)
        character.draw(screen)

        if enemy.health <= 0:
            enemy.alive = False
        
        if enemy.alive:
            enemy.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()