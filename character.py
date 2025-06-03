import pygame
import os
from gcd import gcd


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, attack, health, max_health, speed = 3, width = 70, height= 110, color= (0, 0, 255), boundary_rect=None, is_character = False):
        super().__init__()
        self.x = x
        self.y = y
        self.attack = attack
        self.health = health
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self.boundary_rect = boundary_rect 
        self.is_character = is_character
        self.font = pygame.font.Font(None, 18)
        self.alive = True 
        self.max_health = max_health

         # Animation properties
        self.animation_state = "idle"  # Current animation state ("idle" or "attacking")
        self.idle_frames = []    
        self.running_frames = []      # List to store idle animation frames
        self.attack_frames = []        # List to store attack animation frames
        self.animation_speed = 0.15    # Controls animation speed (lower is faster)
        self.current_frame = 0         # Current frame index
        self.animation_timer = 0       # Timer to control frame changes
        self.is_attacking = False      # Flag to track attacking state
        self.attack_animation_complete = True  # Flag to track if attack animation complet
        # Load animation frames

        self.health_icon = pygame.image.load("assets/toppng.com-ixel-heart-icon-pixel-heart-icon-545x474.png").convert_alpha()
        self.attack_icon = pygame.image.load("assets/pngegg.png").convert_alpha()

        self.attack_icon = pygame.transform.scale(self.attack_icon, (24, 25))
        self.health_icon = pygame.transform.scale(self.health_icon, (20, 17))

        try:
            base_folder = "assets\\Reaper_Man_1\\PNG\\PNG Sequences"
            idle_folder = os.path.join(base_folder, "Idle Blinking")
            running_folder = os.path.join(base_folder, "Running")
            attack_folder = os.path.join(base_folder, "Slashing in The Air")

            self.idle_frames = self.loadAnimationFrames(idle_folder, width, height)
            self.running_frames = self.loadAnimationFrames(running_folder, width, height)

            self.attack_frames = self.loadAnimationFrames(attack_folder, width, height)
            if self.running_frames:
                self.image = self.running_frames[0]
            else:
                raise Exception("No idle animation frames loaded")
        except Exception as e:
            print(f"Failed to load animation frames: {e}")
            # Create colored rectangle as fallback
            self.image = pygame.Surface((width, height))
            
            self.image.fill(color)

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
        # Always allow starting a new attack animation
        self.is_attacking = True
        self.animation_state = "attacking"
        self.current_frame = 0
        self.animation_timer = 0
        self.attack_animation_complete = False

    def updateAnimation(self):
        """Update the current animation frame based on state"""
        # Get the current animation frames based on state
        if self.animation_state == "attacking":
            current_frames = self.attack_frames
        elif self.animation_state == "running":
            current_frames = self.running_frames
        else:
            current_frames = self.idle_frames

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
                    # Loop other animations
                    self.current_frame = 0
            
            # Update the image
            if self.current_frame < len(current_frames):
                self.image = current_frames[self.current_frame]



    def fullHealth(self):
        return self.health

    def attackPower(self):
        return self.attack
    
    #still has an error when the character touches the edge of the screen, the running animation then plays even if you are in idle
    def move(self, target_x, target_y, screen_width, screen_height):
        if not self.alive:
            return

        dx = target_x - self.x
        dy = target_y - self.y

        if dx == 0 and dy == 0:

            if not self.is_attacking:
                self.animation_state = "idle"

            return

        gcd_value = gcd(abs(dx), abs(dy))
        step_x = dx // gcd_value if gcd_value != 0 else 0
        step_y = dy // gcd_value if gcd_value != 0 else 0

        next_x = self.x + step_x * self.speed
        next_y = self.y + step_y * self.speed



        # moved = False  # Track whether the character actually moved

        prev_x, prev_y = self.x, self.y

        if self.boundary_rect:
            if self.boundary_rect.left <= next_x <= self.boundary_rect.right - self.width:
                self.x = next_x

            if self.boundary_rect.top <= next_y <= self.boundary_rect.bottom - self.height:
                self.y = next_y

        else:
            if 0 <= next_x <= screen_width - self.width:
                self.x = next_x

            if 0 <= next_y <= screen_height - self.height:
                self.y = next_y


        moved = (self.x != prev_x) or (self.y != prev_y)

        if not self.is_attacking:
            if moved:
                self.animation_state = "running"
            else:
                self.animation_state = "idle"


        self.rect.topleft = (self.x, self.y)
        self.updateAnimation()


    def takeDamage(self, damage: int):
        """Reduces health and marks enemy as destroyed if needed."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False  
            
    def update(self):
        self.updateAnimation()


    def draw(self, screen):
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

