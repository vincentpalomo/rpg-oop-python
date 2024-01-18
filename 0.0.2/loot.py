import random
from weapon import Weapon, iron_sword, bronze_sword, silver_sword,short_bow, long_bow, recurve_bow, fists, bronze_hammer, morning_star

class Loot:
  def __init__(self) -> None:
    self.weapons = [iron_sword, bronze_sword, silver_sword,short_bow, long_bow, recurve_bow, fists, bronze_hammer, morning_star]

  def get_random_loot(self):
    if not self.weapons:
      return None
    
    random_weapon = random.choice(self.weapons)
    return Weapon(
      name=random_weapon.name,
      weapon_type=random_weapon.weapon_type,
      damage=random_weapon.damage
    )