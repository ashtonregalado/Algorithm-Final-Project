import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, direction=1, speed=5, color=(0, 0, 0), owner=None):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.direction = direction
        self.speed = speed
        self.color = color
        self.owner = owner
        self.active = True

        # Default bullet size
        width = 10
        height = 10
        bullet_sprite = "assets\PNG\Wraith_02\Vector Parts\Spells Effect.png"

        # Customize if bullet is from general or boss
        if self.owner:
            if hasattr(self.owner, "is_general") and self.owner.is_general:
                # self.color = (255, 0, 0)
                bullet_sprite = "assets\PNG\Wraith_01\Vector Parts\Spells Effect.png"
                self.speed = 10
                width = 15
                height = 15
            elif hasattr(self.owner, "is_final_boss") and self.owner.is_final_boss:
                # self.color = (128, 0, 128)
                bullet_sprite = "assets\PNG\Wraith_03\Vector Parts\Spells-Effect.png"
                self.speed = 20
                width = 25
                height = 25
            elif hasattr(self.owner, "is_character"):
                # self.color = (100, 100, 100)
                bullet_sprite = "assets\Reaper_Man_1\PNG\Vector Parts\SlashFX.png"
                self.speed = 10
                width = 15
                height = 15
        self.image = pygame.image.load(bullet_sprite).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))  # Adjust size if needed
        self.rect = pygame.Rect(x, y, width, height)

    # def update(self):
    #     self.rect.x += self.speed * self.direction
    #     self.x = self.rect.x  # keep x in sync
    #     if self.rect.right < 0 or self.rect.left > 800:
    #         self.active = False

    def update(self):
        if self.dx != 0 or self.dy != 0:
            # Use directional dx/dy movement (for boss bullets)
            self.x += self.dx
            self.y += self.dy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
        else:
            # Use horizontal straight movement (for character/general)
            self.rect.x += self.speed * self.direction
            self.x = self.rect.x  # keep x in sync

        # Deactivate if off-screen
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.active = False


        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
