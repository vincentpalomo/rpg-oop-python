# ----------- imports -------------
from weapon import fists
from health_bar import HealthBar

# ----------- parent class ---------------
class Character:
  def __init__(self, name: str, health: int) -> None:
    self.name = name
    self.health = health
    self.max_health = health
    self.health_bar = HealthBar(self)

    self.weapon = fists
  
  def attack(self, target) -> None:
    target.health -= self.weapon.damage
    target.health = max(target.health, 0)
    target.health_bar.update()
    print(f'{self.name} dealt {self.weapon.damage} to {target.name} with {self.weapon.name}')

  def is_dead(self) -> bool:
    return self.health <= 0
  
  def reset(self) -> None:
    self.health = self.max_health
    self.health_bar.update()

# ---------- subclass setup ---------------
class Hero(Character):
  def __init__(self, name: str, health: int, initial_weapon=None) -> None:
    super().__init__(name=name, health=health)

    self.default_weapon = initial_weapon if initial_weapon else self.weapon
    self.weapon = self.default_weapon
    self.health_bar = HealthBar(self, color='green')

    if initial_weapon:
      self.equip(initial_weapon)

  def equip(self, weapon) -> None:
    self.weapon = weapon
    print(f'{self.name} equipped a(n) {self.weapon.name}!')

  def drop(self) -> None:
    print(f'{self.name} dropped the {self.weapon.name}!')
    self.weapon = self.default_weapon

  def reset(self):
    super().reset()
    self.equip(self.default_weapon)

class Enemy(Character):
  def __init__(self, name: str, health: int, weapon) -> None:
    super().__init__(name, health)
    
    self.weapon = weapon
    self.health_bar = HealthBar(self, color='red')