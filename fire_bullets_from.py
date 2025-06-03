from bullet import Bullet

def fireBulletsFrom(enemy, bullets_list):
    if enemy.attack_animation_complete:
        enemy.startAttackAnimation()

        num_bullets = 1
        spread_gap = 5

        if hasattr(enemy, "is_final_boss") and enemy.is_final_boss:
            num_bullets = 5
            spread_gap = 10
        elif hasattr(enemy, "is_general") and enemy.is_general:
            num_bullets = 2
            spread_gap = 40
        # Determines the vertical offset of the topmost bullet
        start_offset = -((num_bullets - 1) // 2) * spread_gap

        for i in range(num_bullets):
            y_offset = start_offset + i * spread_gap
            x = enemy.x - 10
            y = enemy.y + y_offset

            # Set direction for each bullet
            if hasattr(enemy, "is_final_boss") and enemy.is_final_boss:
                # Top bullet
                if i == 0:
                    bullet = Bullet(x, y, dx=-4, dy=-4, owner=enemy)  # up-left
                # Middle bullet
                elif i == 1:
                    bullet = Bullet(x, y, dx=-4, dy=-2, owner=enemy)
                elif i == 2:
                    bullet = Bullet(x, y, dx=-4, dy=0, owner=enemy)  # straight left
                # Bottom bullet
                elif i == 3:
                    bullet = Bullet(x, y, dx=-4, dy=2, owner=enemy)  # down-left
                else:
                    bullet = Bullet(x, y, dx=-4, dy=4, owner=enemy)
            else:
                bullet = Bullet(x, y, dx=-5, dy=0, owner=enemy)  # straight bullets for others

            bullets_list.append(bullet)