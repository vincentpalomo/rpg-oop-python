import time
import os
from character import Hero, Enemy
from loot import Loot
from weapon import morning_star


class GameLoop:
    def __init__(self, hero, enemy) -> None:
        self.hero = hero
        self.enemy = enemy

    def battle(self):
        os.system('clear')
        print()
        print(f'{"~" * 10} {self.hero.name} vs {self.enemy.name} {"~" * 10}')
        print()
        print(f'{"~" * 10} Prepare for battle! {"~" * 10}')
        time.sleep(2)

        while self.hero.is_alive() and self.enemy.is_alive():
            os.system('clear')
            print()
            self.hero.display_health()
            self.enemy.display_health()

            print()
            hero_damage = self.hero.attack()
            enemy_damage = self.enemy.attack()
            time.sleep(1)

            self.enemy.take_damage(hero_damage)
            if self.hero.weapon is not None:
                print(f'{self.hero.name} deals {hero_damage} to {self.enemy.name} with {self.hero.weapon.name}!')
            else:
                print(f'{self.hero.name} deals {hero_damage} to {self.enemy.name}!')
            time.sleep(1)

            if not self.enemy.is_alive():
                os.system('clear')
                print()
                print(f'{"~" * 10} {self.enemy.name} has been defeated! 💀 {"~" * 10}')
                time.sleep(2)
                
                os.system('clear')
                loot = Loot()
                get_loot = loot.get_random_loot()
                print()
                print(f'You obtained a(n) {get_loot.name}!')
                print()
                answer = input('Do you want to equip the loot? (yes/no): ')
                if answer.lower() == 'yes':
                  hero.equip(get_loot)
                else:
                  print()
                  print(f'The loot was not equipped.')
                time.sleep(2)
                break

            self.hero.take_damage(enemy_damage)
            print(f'{self.enemy.name} deals {enemy_damage} to {self.hero.name}!')
            time.sleep(1)

            if not self.hero.is_alive():
                os.system('clear')
                print()
                print(f'{"~" * 10} {self.hero.name} has been defeated! 💀 {"~" * 10}')
                time.sleep(2)

                os.system('clear')
                print()
                print(f'{"~" * 10} YOU LOSE {"~" * 10}')
                if self.hero.weapon is not None:
                  print()
                  print(f'Your weapon ({self.hero.weapon.name}) has been lost!')
                  self.hero.player_down()
                  time.sleep(2)
                time.sleep(2)
                break

            print()
            input('Press any button to continue...')

        os.system('clear')
        print()
        print(f'Stage Complete!')
        print()
        self.hero.display_health()
        self.enemy.display_health()
        

    def start_game(self):
        while True:
            os.system('clear')
            print()
            print('Welcome to Heroes of Jinxton ⚔')
            print()
            input('Press Enter to Start!')
            self.battle()

            print()
            play_again = input('Do you want to play again? (yes/no): ')

            if play_again.lower() != 'yes':
                break
            else:
                os.system('clear')
                self.hero.reset()
                self.enemy.reset()


hero = Hero(name='Hero', health=100, damage=25)
enemy = Enemy(name='Enemy', health=100, damage=30)

game = GameLoop(hero, enemy)
game.start_game()
