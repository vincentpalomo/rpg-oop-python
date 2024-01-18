from weapon import Weapon
import random

class Loot:
  def __init__(self) -> None:
    self.weapons = []

  def add_weapon(self, weapon):
    self.weapons.append(weapon)

  def get_random_loot(self):
    if not self.weapons:
      return None
    random_weapon = random.choice(self.weapons)
    return Weapon(
      name=f'loot {random_weapon.name}',
      weapon_type=random_weapon.weapon_type,
      damage=random_weapon.damage,
      value=random_weapon.value
    )