import pygame
import math
import random
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, attack, health, max_health, width=80, height=120, color=(255, 0, 0), boundary_rect=None, is_general=False, is_final_boss=False):
        super().__init__()
        self.x = x
        self.y = y
        self.attack = attack
        self.health = health
        self.max_health = max_health
        self.width = width
        self.height = height
        self.color = color
        self.font = pygame.font.Font(None, 18)
        self.alive = True
        self.last_fire_time = pygame.time.get_ticks()
        self.fire_delay = random.randint(500, 1500)
        self.is_general = is_general
        self.is_final_boss = is_final_boss

        self.direction = -1

        self.health_icon = pygame.image.load("assets/toppng.com-ixel-heart-icon-pixel-heart-icon-545x474.png").convert_alpha()
        self.attack_icon = pygame.image.load("assets/pngegg.png").convert_alpha()

        self.attack_icon = pygame.transform.scale(self.attack_icon, (24, 25))
        self.health_icon = pygame.transform.scale(self.health_icon, (20, 17))

        
        # Adjust speed based on enemy type
        if is_final_boss:
            self.speed = 1.5  # Boss moves slower
        elif is_general:
            self.speed = 2  # Generals have medium speed
        else:
            self.speed = 2.5  # Regular soldiers are fastest

        # Set up random movement direction
        while True:
            self.dx = random.choice([-1, 1]) * self.speed
            self.dy = random.choice([-1, 1]) * self.speed
            if self.dx != 0 and self.dy != 0:
                break

        self.boundary = boundary_rect
        
        # Animation properties
        self.animation_state = "idle"  # Current animation state ("idle" or "attacking")
        self.idle_frames = []          # List to store idle animation frames
        self.attack_frames = []        # List to store attack animation frames
        self.animation_speed = 0.15    # Controls animation speed (lower is faster)
        self.current_frame = 0         # Current frame index
        self.animation_timer = 0       # Timer to control frame changes
        self.is_attacking = False      # Flag to track attacking state
        self.attack_animation_complete = True  # Flag to track if attack animation complet
        # Load animation frames
        try:
            # Determine which folder to use based on enemy type
            if is_final_boss:
                base_folder = "assets\\PNG\\Wraith_03\\PNG Sequences"
            elif is_general:
                base_folder = "assets\\PNG\\Wraith_01\\PNG Sequences"
            else:
                base_folder = "assets\\PNG\\Wraith_02\\PNG Sequences"
            
            idle_folder = os.path.join(base_folder, "Idle Blink")
            attack_folder = os.path.join(base_folder, "Attacking")
            
            # Load idle animation frames
            self.idle_frames = self.loadAnimationFrames(idle_folder, width, height)
            
            # Load attack animation frames
            self.attack_frames = self.loadAnimationFrames(attack_folder, width, height)
            
            # Set initial image
            if self.idle_frames:
                self.image = self.idle_frames[0]
            else:
                raise Exception("No idle animation frames loaded")
                
        except Exception as e:
            print(f"Failed to load animation frames: {e}")
            # Create colored rectangle as fallback
            self.image = pygame.Surface((width, height))
            
            # Different colors for different enemy types
            if is_final_boss:
                self.image.fill((200, 0, 0))  # Dark red for boss
            elif is_general:
                self.image.fill((255, 165, 0))  # Orange for generals
            else:
                self.image.fill(color)  # Default red for soldiers

        # Create the rectangle for positioning and collisions
        self.rect = self.image.get_rect(topleft=(x, y))

    def loadAnimationFrames(self, folder_path, width, height):
        """Helper method to load animation frames from a folder"""
        frames = []
        try:
            # Get a list of animation files (sorted to ensure correct order)
            animation_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
            
            # Load each frame
            for frame_file in animation_files:
                frame_path = os.path.join(folder_path, frame_file)
                frame = pygame.image.load(frame_path)
                frame = pygame.transform.scale(frame, (width, height))
                frames.append(frame)
                
        except Exception as e:
            print(f"Failed to load frames from {folder_path}: {e}")
            
        return frames

    def startAttackAnimation(self):
        """Start the attack animation sequence"""
        if not self.is_attacking and self.attack_animation_complete:
            self.is_attacking = True
            self.animation_state = "attacking"
            self.current_frame = 0
            self.animation_timer = 0
            self.attack_animation_complete = False

    def updateAnimation(self):
        """Update the current animation frame based on state"""
        # Get the current animation frames based on state
        current_frames = self.attack_frames if self.animation_state == "attacking" else self.idle_frames
        
        if not current_frames:
            return
            
        self.animation_timer += 0.1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            
            # Advance to next frame
            self.current_frame += 1
            
            # Check if we've reached the end of the animation
            if self.current_frame >= len(current_frames):
                # If attacking, go back to idle after attack animation completes
                if self.animation_state == "attacking":
                    self.animation_state = "idle"
                    self.is_attacking = False
                    self.attack_animation_complete = True
                    self.current_frame = 0
                else:
                    # Loop idle animation
                    self.current_frame = 0
            
            # Update the image
            if self.current_frame < len(current_frames):
                self.image = current_frames[self.current_frame]


    def fullHealth(self):
        return self.health
    
    def attackPower(self):
        return self.attack
    
    @staticmethod
    def randomDirection(speed):
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle) * speed, math.sin(angle) * speed

    def move(self):
        if not self.alive:
            return

        # Move using float precision
        self.x += self.dx
        self.y += self.dy

        # Update rect for display (use int conversion for rendering)
        self.rect.topleft = (int(self.x), int(self.y))

        if self.boundary:
            bounced = False

            # Create a temp rect from float x/y
            temp_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

            if not self.boundary.contains(temp_rect):
                temp_rect.clamp_ip(self.boundary)
                self.x, self.y = temp_rect.topleft
                bounced = True

            # Left/right
            if temp_rect.left <= self.boundary.left:
                self.x = self.boundary.left
                bounced = True
            elif temp_rect.right >= self.boundary.right:
                self.x = self.boundary.right - self.width
                bounced = True

            # Top/bottom
            if temp_rect.top <= self.boundary.top:
                self.y = self.boundary.top
                bounced = True
            elif temp_rect.bottom >= self.boundary.bottom:
                self.y = self.boundary.bottom - self.height
                bounced = True

            if bounced:
                self.dx, self.dy = self.randomDirection(self.speed)

        self.rect.topleft = (int(self.x), int(self.y))
        
        # Update animation
        self.updateAnimation()

    def fire(self):
        """Called when the enemy fires a bullet"""
        self.startAttackAnimation()
        return True  # Return True to indicate firing action taken


    def takeDamage(self, damage: int):
        """Reduces health and marks enemy as destroyed if needed."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False  
            
    def update(self):
        """Update method required for sprite groups"""
        self.updateAnimation()

    def draw(self, screen):
        """Draws the enemy, displaying attack above and health in the middle."""
        if self.alive:
            screen.blit(self.image, self.rect.topleft)
            padding = 5

            # ---- Health (topmost) ----
            health_surface = self.font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
            health_icon_rect = self.health_icon.get_rect()
            health_rect = health_surface.get_rect()

            # Position icon first (above sprite)
            health_icon_rect.topleft = (self.rect.left + padding, self.rect.top - 40)
            # Align text to right of icon
            health_rect.midleft = (health_icon_rect.right + 8, health_icon_rect.centery)

            screen.blit(self.health_icon, health_icon_rect)
            screen.blit(health_surface, health_rect)

            # ---- Attack (just below health) ----
            attack_surface = self.font.render(f"{self.attack}", True, (255, 255, 255))
            attack_icon_rect = self.attack_icon.get_rect()
            attack_rect = attack_surface.get_rect()

            # Position icon just below health icon
            attack_icon_rect.topleft = (self.rect.left + padding, health_icon_rect.bottom + 5)
            # Align text to right of icon
            attack_rect.midleft = (attack_icon_rect.right + 5, attack_icon_rect.centery)

            screen.blit(self.attack_icon, attack_icon_rect)
            screen.blit(attack_surface, attack_rect)

        return self.alive