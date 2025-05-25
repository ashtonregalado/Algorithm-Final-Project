import pygame

current_bg_index = 0
next_bg_index = 1
fade_alpha = 0
fading = False
fade_speed = 1
last_fade_time = pygame.time.get_ticks()
fade_interval = 1500  # milliseconds


def draw_background(screen, backgrounds):
    global current_bg_index, next_bg_index, fade_alpha, fading, last_fade_time

    now = pygame.time.get_ticks()

    # Start fading after fade_interval
    if not fading and now - last_fade_time > fade_interval:
        fading = True
        fade_alpha = 0
        next_bg_index = (current_bg_index + 1) % len(backgrounds)

    if fading:
        # Draw current background
        screen.blit(backgrounds[current_bg_index], (0, 0))

        # Fade in the next background
        fade_surface = backgrounds[next_bg_index].copy()
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha += fade_speed

        if fade_alpha >= 255:
            fading = False
            current_bg_index = next_bg_index
            last_fade_time = now
    else:
        screen.blit(backgrounds[current_bg_index], (0, 0))