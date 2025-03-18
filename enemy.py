import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, width=40, height=90, color=(255, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.width = width
        self.height = height
        self.color = color
        self.font = pygame.font.Font(None, 18)
        self.alive = True  # Tracks if enemy is still active

        # Load enemy sprite (fallback to rectangle if not using images)
        try:
            self.image = pygame.image.load("assets/enemy.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.rect = self.image.get_rect(topleft=(x, y))

    def full_health(self):
        return self.health

    def take_damage(self, damage: int):
        """Reduces health and marks enemy as destroyed if needed."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False  # Mark enemy as destroyed
            

    def draw(self, screen):
        """Draws the enemy and displays health if it's still alive."""
        if self.alive:
            screen.blit(self.image, self.rect.topleft)

            # Center the text on the enemy
            text_surface = self.font.render(str(self.health), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
