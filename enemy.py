import pygame
import math
import random
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, attack, health, width=80, height=120, color=(255, 0, 0), boundary_rect=None, is_general=False, is_final_boss=False):
        super().__init__()
        self.x = x
        self.y = y
        self.attack = attack
        self.health = health
        self.max_health = health
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
        
        # Adjust speed based on enemy type
        if is_final_boss:
            self.speed = 1  # Boss moves slower
        elif is_general:
            self.speed = 1.5  # Generals have medium speed
        else:
            self.speed = 2  # Regular soldiers are fastest

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
            self.idle_frames = self._load_animation_frames(idle_folder, width, height)
            
            # Load attack animation frames
            self.attack_frames = self._load_animation_frames(attack_folder, width, height)
            
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

    def _load_animation_frames(self, folder_path, width, height):
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

    def start_attack_animation(self):
        """Start the attack animation sequence"""
        if not self.is_attacking and self.attack_animation_complete:
            self.is_attacking = True
            self.animation_state = "attacking"
            self.current_frame = 0
            self.animation_timer = 0
            self.attack_animation_complete = False

    def update_animation(self):
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


    def full_health(self):
        return self.health
    
    def attack_power(self):
        return self.attack
    
    @staticmethod
    def random_direction(speed):
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
                self.dx, self.dy = self.random_direction(self.speed)

        self.rect.topleft = (int(self.x), int(self.y))
        
        # Update animation
        self.update_animation()

    def fire(self):
        """Called when the enemy fires a bullet"""
        self.start_attack_animation()
        return True  # Return True to indicate firing action taken


    def take_damage(self, damage: int):
        """Reduces health and marks enemy as destroyed if needed."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False  
            
    def update(self):
        """Update method required for sprite groups"""
        self.move()

    def draw(self, screen):
        """Draws the enemy, displaying attack above and health in the middle."""
        if self.alive:
            screen.blit(self.image, self.rect.topleft)

            attack_surface = self.font.render(f"ATK: {self.attack}", True, (0, 0, 0))
            attack_rect = attack_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
            screen.blit(attack_surface, attack_rect)

            # Draw visual health bar
            health_bar_width = self.width
            health_bar_height = 6
            health_bar_x = self.rect.x
            health_bar_y = self.rect.y - 10
            
            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), 
                             (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            
            # Foreground (green) - sized according to current health
            health_percent = max(0, self.health / self.max_health)
            current_health_width = health_bar_width * health_percent
            pygame.draw.rect(screen, (0, 255, 0), 
                             (health_bar_x, health_bar_y, current_health_width, health_bar_height))

            # Also show health number
            health_surface = self.font.render(f"{self.health}", True, (255, 255, 255))
            health_rect = health_surface.get_rect(center=self.rect.center)
            screen.blit(health_surface, health_rect)

        return self.alive