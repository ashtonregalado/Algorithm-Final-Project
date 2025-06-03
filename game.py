import pygame
import random
from character import Character
from enemy import Enemy
from damage import Damage
from damageGameplay import  enemyDamageGameplay, characterDamageGameplay
from bullet import Bullet
from damage_text import DamageText
from gcd import gcd
from game_over import gameOver
from start_menu import startMenu
from fire_bullets_from import fireBulletsFrom

pygame.init()

WIDTH,HEIGHT = 850, 650
grid_size = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Euclid's Algorithm")

WHITE = (255, 255, 255)

soldier_background = pygame.image.load("assets/enemy-background/Space Background.png").convert()
general_background = pygame.image.load("assets/enemy-background/Vhv4XI.png").convert()
final_boss_background = pygame.image.load("assets/enemy-background/G7zxxR.png").convert()


soldier_background = pygame.transform.scale(soldier_background, (WIDTH, HEIGHT))
general_background = pygame.transform.scale(general_background, (WIDTH, HEIGHT))
final_boss_background = pygame.transform.scale(final_boss_background, (WIDTH, HEIGHT))

character_boundary = pygame.Rect(0, 0, WIDTH // 2, HEIGHT)
enemy_boundary = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)


backgrounds = [soldier_background, general_background, final_boss_background]


def main():

    soldier_1 = Enemy(700, 100, 25, 250, 250, boundary_rect=enemy_boundary)
    soldier_2 = Enemy(700, 200, 25, 250, 250, boundary_rect=enemy_boundary)
    soldier_3 = Enemy(700, 300, 25, 250,250, boundary_rect=enemy_boundary)
    soldier_4 = Enemy(700, 400, 25, 250,250, boundary_rect=enemy_boundary)
    soldier_5 = Enemy(700, 500, 25, 250,250, boundary_rect=enemy_boundary)

    general_1 = Enemy(700, 200, 50, 500, 500,boundary_rect=enemy_boundary, is_general = True)
    general_2 = Enemy(700, 400, 50, 500,500, boundary_rect=enemy_boundary, is_general = True)
    general_3 = Enemy(700, 600, 50, 500,500, boundary_rect=enemy_boundary, is_general = True)

    final_boss = Enemy(700, 400, 150, 1000,1000, boundary_rect=enemy_boundary, is_final_boss=True)

    enemies = [[soldier_1, soldier_2, soldier_3, soldier_4, soldier_5], [general_1, general_2, general_3], final_boss]

    character = Character(200, 400, 45, 500, 500,boundary_rect=character_boundary, is_character=True)

    character_bullets = []
    character_damage_texts = []
    enemy_bullets = []
    enemy_damage_texts = []

    running = True
    clock = pygame.time.Clock()
    target_x, target_y = character.x, character.y

    wave_index = 0
    current_wave = enemies[wave_index] if isinstance(enemies[wave_index], list) else [enemies[wave_index]]

    while running:
        if wave_index == 0:
            screen.blit(soldier_background, (0, 0))
        elif wave_index == 1:
            screen.blit(general_background, (0, 0))
        else:
            screen.blit(final_boss_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and character.alive:
                    if character.attack_animation_complete:
                        character.startAttackAnimation()
                        character_bullets.append(Bullet(character.x + 20, character.y + 10,0,0, owner=character))


            if event.type == pygame.MOUSEBUTTONDOWN:
                if character.attack_animation_complete:
                    character.startAttackAnimation()
                    character_bullets.append(Bullet(character.x + 20, character.y + 10,0,0, owner=character))

        current_time = pygame.time.get_ticks()
        for enemy in current_wave:
            if enemy.alive and current_time - enemy.last_fire_time >= enemy.fire_delay:
                fireBulletsFrom(enemy, enemy_bullets)
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
                        enemyDamageGameplay(enemy, character)
                        if enemy.alive:
                            character_damage_texts.append(DamageText(
                                enemy.x + 10, enemy.y - 20,
                                Damage.damage(character.attack, enemy.health)
                            ))

        if character.alive:
            for bullet in enemy_bullets[:]:
                if bullet.rect.colliderect(character.rect):
                    enemy_bullets.remove(bullet)
                    characterDamageGameplay( character, bullet.owner)
                    if character.alive:
                        enemy_damage_texts.append(DamageText(character.x + 10, character.y + -20, Damage.damage(bullet.owner.attack, character.health)))
            
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
            character.update()
            character.draw(screen)


        for enemy in current_wave:
            if enemy.health <= 0:
                enemy.alive = False
        for enemy in current_wave:
            if enemy.alive:
                enemy.move()
                enemy.update()
                enemy.draw(screen)

        # Check if all enemies in the current wave are dead
        if all(not e.alive for e in current_wave):
            wave_gcd_attack_bonus = sum(gcd(character.attack, e.attack) for e in current_wave)
            wave_gcd_health_bonus = sum(gcd(character.health, e.max_health)for e in current_wave)
            character.attack += wave_gcd_attack_bonus
            character.health += wave_gcd_health_bonus
            character.max_health += wave_gcd_health_bonus


            wave_index += 1
            if wave_index < len(enemies):
                next_wave = enemies[wave_index]
                current_wave = next_wave if isinstance(next_wave, list) else [next_wave]
                # Optional: reset bullets and damage text for clarity
                enemy_bullets.clear()
                enemy_damage_texts.clear()
            else:
                print("YOU WIN!")
                gameOver(screen, WIDTH, HEIGHT, "character")
                
                running = False
                return

        if not character.alive:
            gameOver(screen, WIDTH, HEIGHT, "enemy")
            return

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def runGame():
    while True:
        startMenu(screen, backgrounds, WIDTH, HEIGHT)
        main()

if __name__ == "__main__":
    pygame.init()
    runGame()
