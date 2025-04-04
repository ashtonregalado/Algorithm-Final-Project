from gcd import gcd

class Damage:
    @staticmethod
    def damage(attack: int, health: int) -> int:
        total_damage = gcd(attack, health)

        return total_damage
