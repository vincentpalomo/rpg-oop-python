import time
import os
from character import Hero, Enemy

class GameLoop:
  def __init__(self, hero, enemy) -> None:
    self.hero = hero
    self.enemy = enemy

  def battle(self):
    print(f'{self.hero.name} vs {self.enemy.name}')

    while self.hero.is_alive() and self.enemy.is_alive():
      os.system('clear')
      print()
      self.hero.display_health()
      self.enemy.display_health()

      print()
      hero_damage = self.hero.attack()
      enemy_damage = self.enemy.attack()

      self.enemy.take_damage(hero_damage)
      print(f'{self.hero.name} deals {hero_damage} to {self.enemy.name}!')
      time.sleep(1)

      if not self.enemy.is_alive():
        print(f'{self.enemy.name} has been defeated!')
        break

      self.hero.take_damage(enemy_damage)
      print(f'{self.enemy.name} deals {enemy_damage} to {self.hero.name}!')
      time.sleep(1)

      if not self.hero.is_alive():
        print(f'{self.hero.name} has been defeated!')
        break

      input()

    os.system('clear')
    print()
    print(f'Stage Complete!')
    self.hero.display_health()
    self.enemy.display_health()

  def start_game(self):
    print('Welcome to hero of jinx')
    self.battle()

hero = Hero(name='Doo', health=100, damage=25)
enemy = Enemy(name='Wormy', health=100, damage=15)

game = GameLoop(hero, enemy)
game.start_game()