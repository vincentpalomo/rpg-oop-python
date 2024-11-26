import random
from game.weapon import Weapon, get_weapons


class Loot:
    def __init__(self) -> None:
        self.weapons = get_weapons

    def get_random_loot(self):
        if not self.weapons:
            return None

        random_weapon = random.choice(self.weapons)
        return Weapon(
            name=random_weapon.name,
            weapon_type=random_weapon.weapon_type,
            damage=random_weapon.damage
        )
