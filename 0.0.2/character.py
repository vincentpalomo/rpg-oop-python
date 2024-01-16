import random

class Character:
  def __init__(self, name, health, damage, weapon=None) -> None:
    self.name = name
    self.health = health
    self.damage = damage
    self.weapon = weapon

  def attack(self) -> None:
    is_critical = random.random() < 0.1

    if is_critical:
      print(f'!CRITICAL HIT!')
      print()
      return int(self.damage * 1.5)
    else:
      return random.randint(1, self.damage)
    
  def take_damage(self, damage) -> None:
    self.health -= damage

    if self.health < 0:
      self.health = 0

  def is_alive(self) -> None:
    return self.health > 0
  
  def display_health(self):
    bar_length = 20
    remaining_health = int((self.health / 100) * bar_length)
    health_bar = '[' + '#' * remaining_health + '-' * (bar_length - remaining_health) + ']'
    print(f'{self.name}`s HP: {health_bar} {self.health}')

  def reset(self) -> None:
    self.health = self.health

class Hero(Character):
  def __init__(self, name, health, damage, weapon=None) -> None:
    super().__init__(name, health, damage, weapon)

  def reset(self):
    super().reset()

class Enemy(Character):
  def __init__(self, name, health, damage, weapon=None) -> None:
    super().__init__(name, health, damage, weapon)