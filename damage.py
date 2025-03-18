from gcd import gcd

class Damage:
    @staticmethod
    def damage(character_attack: int, enemy_health: int) -> int:
        total_damage = gcd(character_attack, enemy_health)

        return total_damage
