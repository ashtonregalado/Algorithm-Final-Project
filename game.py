import pygame
import random
from character import Character
from enemy import Enemy
from damage import Damage
from gameplay import  EnemyDamageGameplay, CharacterDamageGameplay
from bullet import Bullet
from damage_text import DamageText
from gcd import gcd
from adjust_stats import AdjustStats

pygame.init()

WIDTH,HEIGHT = 800, 600
grid_size = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Euclid's Algorithm")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

character_boundary = pygame.Rect(0, 0, WIDTH // 2, HEIGHT)
enemy_boundary = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)

soldier_1 = Enemy(700, 200, 50, 200, boundary_rect=enemy_boundary)
soldier_2 = Enemy(700, 400, 50, 200, boundary_rect=enemy_boundary)
soldier_3 = Enemy(700, 600, 50, 200, boundary_rect=enemy_boundary)

general_1 = Enemy(700, 200, 100, 500, boundary_rect=enemy_boundary, is_general = True)
general_2 = Enemy(700, 600, 100, 500, boundary_rect=enemy_boundary, is_general = True)

final_boss = Enemy(700, 400, 500, 1000, boundary_rect=enemy_boundary, is_final_boss=True)

enemies = [[soldier_1, soldier_2, soldier_3], [general_1, general_2], final_boss]

character = Character(200, 400, 100, 1312, boundary_rect=character_boundary, is_character=True)

character_bullets = []
character_damage_texts = []
enemy_bullets = []
enemy_damage_texts = []

def fire_bullets_from(enemy, bullets_list):
    num_bullets = 1
    spread_gap = 5  # vertical gap between each bullet in pixels

    if hasattr(enemy, "is_final_boss") and enemy.is_final_boss:
        num_bullets = 3
        spread_gap = 100
    elif hasattr(enemy, "is_general") and enemy.is_general:
        num_bullets = 2
        spread_gap = 40

    print(f"Firing {num_bullets} bullets from {'Final Boss' if enemy.is_final_boss else 'General' if enemy.is_general else 'Soldier'}")
    
    start_offset = -((num_bullets - 1) // 2) * spread_gap

    for i in range(num_bullets):
        y_offset = start_offset + i * spread_gap
        bullet = Bullet(enemy.x - 10, enemy.y + y_offset, direction=-1, owner=enemy)
        bullets_list.append(bullet)
    



def main():
    running = True
    clock = pygame.time.Clock()
    target_x, target_y = character.x, character.y
    enemy_fire_delay = random.randint(10, 1000)
    last_enemy_fire_time = pygame.time.get_ticks()

    wave_index = 0
    current_wave = enemies[wave_index] if isinstance(enemies[wave_index], list) else [enemies[wave_index]]

    print(enemy_fire_delay)

    while running:
        screen.fill(WHITE)

        # character_add_button = AdjustStats.addAttackButton(screen)
        # character_subtract_button = AdjustStats.subtractAttackButton(screen)
        # enemy_add_button = AdjustStats.addHealthButton(screen)
        # enemy_subtract_button = AdjustStats.subtractHealthButton(screen)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and character.alive:
                    character_bullets.append(Bullet(character.x + 20, character.y + 10, owner=character))




            if event.type == pygame.MOUSEBUTTONDOWN:

               
                # if character_add_button.collidepoint(event.pos):
                #         character.attack += 1

                # elif character_subtract_button.collidepoint(event.pos):
                #     character.attack -= 1

                # # Check enemy buttons independently
                # for enemy in current_wave:
                #     if enemy_add_button.collidepoint(event.pos):
                #         enemy.health += 1
                #     if enemy_subtract_button.collidepoint(event.pos):
                #         enemy.health -= 1
                    
                # if not (character_add_button.collidepoint(event.pos) or 
                #           character_subtract_button.collidepoint(event.pos) or 
                #           enemy_add_button.collidepoint(event.pos) or 
                #           enemy_subtract_button.collidepoint(event.pos) ) and  character.alive:
                character_bullets.append(Bullet(character.x + 20, character.y + 10, owner=character))

        current_time = pygame.time.get_ticks()
        for enemy in current_wave:
            if enemy.alive and current_time - enemy.last_fire_time >= enemy.fire_delay:
                fire_bullets_from(enemy, enemy_bullets)
                print(f"Bullets after firing: {len(enemy_bullets)}")
                enemy.last_fire_time = current_time
                enemy.fire_delay = random.randint(500, 1500)

            
            
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            target_x -= character.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            target_x += character.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            target_y -= character.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            target_y += character.speed


        for bullet in character_bullets:
            bullet.update()

        for bullet in enemy_bullets:
            bullet.update()

        for enemy in current_wave:
            if enemy.alive:
                for bullet in character_bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        character_bullets.remove(bullet)
                        EnemyDamageGameplay(enemy, character)
                        if enemy.alive:
                            character_damage_texts.append(DamageText(
                                enemy.x + 10, enemy.y - 20,
                                Damage.damage(character.attack, enemy.health)
                            ))

            
        if character.alive:
            for bullet in enemy_bullets[:]:
                if bullet.rect.colliderect(character.rect):
                    enemy_bullets.remove(bullet)
                    CharacterDamageGameplay( character, enemy)
                    if character.alive:
                        enemy_damage_texts.append(DamageText(character.x + 10, character.y + -20, Damage.damage(enemy.attack, character.health)))
            
        character_bullets[:] = [bullet for bullet in character_bullets if bullet.active]
        enemy_bullets[:] = [bullet for bullet in enemy_bullets if bullet.active]

        for bullet in character_bullets:
            bullet.draw(screen)
        
        for bullet in enemy_bullets:
            bullet.draw(screen)

        for dmg in character_damage_texts[:]:
            dmg.update()
            if dmg.duration <= 0:
                character_damage_texts.remove(dmg)

        for dmg in enemy_damage_texts[:]:
            dmg.update()
            if dmg.duration <= 0:
                enemy_damage_texts.remove(dmg)

        for dmg in character_damage_texts:
            dmg.draw(screen)

        for dmg in enemy_damage_texts:
            dmg.draw(screen)

        if character.health <= 0:
            character.alive = False
        
        if character.alive:
            character.move(target_x, target_y, WIDTH, HEIGHT)
            character.draw(screen)


        for enemy in current_wave:
            if enemy.health <= 0:
                enemy.alive = False
        for enemy in current_wave:
            if enemy.alive:
                enemy.move()
                enemy.draw(screen)

        # Check if all enemies in the current wave are dead
        if all(not e.alive for e in current_wave):
            wave_gcd_attack_bonus = sum(gcd(character.attack, e.attack) for e in current_wave)
            wave_gcd_health_bonus = sum(gcd(character.health, e.max_health)for e in current_wave)
            character.attack += wave_gcd_attack_bonus
            character.health += wave_gcd_health_bonus


            
            wave_index += 1
            if wave_index < len(enemies):
                next_wave = enemies[wave_index]
                current_wave = next_wave if isinstance(next_wave, list) else [next_wave]
                # Optional: reset bullets and damage text for clarity
                enemy_bullets.clear()
                enemy_damage_texts.clear()
            else:
                print("YOU WIN!")
                running = False

        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()