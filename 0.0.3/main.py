import time
import os
import cutie
from pyfiglet import Figlet
from character import Hero, Enemy 
from enemy import Random_Enemy 
from loot import Loot

custom_fig = Figlet(font='roman')
bubble = Figlet(font='digital')

class GameLoop:
    def __init__(self, hero, enemy) -> None:
        self.hero = hero
        self.enemy = enemy
        self.stage = 1
        self.enemy_damage_increase = 0
        self.enemy_health_increase = 0
        self.loss = False

    def increment_stage(self):
        self.stage += 1

    def battle(self):
        os.system('clear')
        print()
        print(f'      {"~" * 10} {self.hero.name} vs {self.enemy.name} {"~" * 10}')
        print()
        print(f'                    Stage: {self.stage}                      ')
        print()
        if self.enemy_damage_increase != 0:
            print(f'     Enemy damage increased by: +{self.enemy_damage_increase}')
            print()

        if self.enemy_health_increase != 0:
            print(f'     Enemy health increased by: +{self.enemy_health_increase}')

        print(bubble.renderText('     Prepare for battle      '))
        time.sleep(2)

        while self.hero.is_alive() and self.enemy.is_alive():
            os.system('clear')
            print()
            self.hero.display_health()
            if self.hero.weapon is not None:
                print(f'        Current base damage: {self.hero.damage + self.hero.weapon.damage}')
            else:
                print(f'        Current base damage: {self.hero.damage}')
            self.enemy.display_health()
            print(f'        Enemy current base damage: {self.enemy.damage}')

            print()
            hero_damage = self.hero.attack()
            enemy_damage = self.enemy.attack()
            time.sleep(1)

            self.enemy.take_damage(hero_damage)
            if self.hero.weapon is not None:
                print(f'        {self.hero.name} deals {hero_damage} to {self.enemy.name} with {self.hero.weapon.name}!')
            else:
                print(f'        {self.hero.name} deals {hero_damage} to {self.enemy.name}!')
            time.sleep(1)

            if not self.enemy.is_alive():
                os.system('clear')
                print()
                print(f'    {"~" * 10} {self.enemy.name} has been defeated! 💀 {"~" * 10}')
                # self.enemy.increase_damage()
                if self.stage % 2 == 1:
                    print()
                    print(f'    enemy has gained +5 damage!')
                    self.enemy_damage_increase += 5
                if self.stage % 5 == 0:
                    print()
                    print(f'    enemy has gained +15 health!')
                    self.enemy_health_increase += 15
                self.increment_stage()

                if self.stage % 10 == 0:
                    self.hero.increase_damage()

                self.hero.increase_health()
                time.sleep(3)
                
                os.system('clear')
                loot = Loot()
                get_loot = loot.get_random_loot()
                print()
                print(f'        You obtained a(n) {get_loot.name}! +{get_loot.damage} damage')
                print()
                
                if cutie.prompt_yes_or_no('     Do you want to equip the loot? '):
                    hero.equip(get_loot)
                else:
                    print()
                    print(f'        The loot was not equipped.')

                # answer = input('        Do you want to equip the loot? (yes/no): ')
                # if answer.lower() == 'yes':
                #   hero.equip(get_loot)
                # else:
                #   print()
                #   print(f'      The loot was not equipped.')
                time.sleep(2)
                break

            self.hero.take_damage(enemy_damage)
            print(f'        {self.enemy.name} deals {enemy_damage} to {self.hero.name}!')
            time.sleep(1)

            if not self.hero.is_alive():
                os.system('clear')
                print()
                print(f'        {"~" * 10} {self.hero.name} has been defeated! 💀 {"~" * 10}')
                time.sleep(2)

                os.system('clear')
                print()
                # print(f'        {"~" * 10} YOU LOSE {"~" * 10}')
                print(bubble.renderText('       You Lose       '))
                if self.hero.weapon is not None:
                  print()
                  print(f'  Your weapon ({self.hero.weapon.name}) has been lost!')
                  print()
                  self.hero.player_down()
                  self.enemy.reset_damage()
                  time.sleep(2)
                print()
                print(f'    You made it to stage: {self.stage}      ') 
                self.stage = 1
                self.loss = True
                self.enemy_damage_increase = 0
                self.enemy_health_increase = 0
                time.sleep(2)
                break

            print()
            input('     Press any button to continue...')

        os.system('clear')
        print()
        # print(f'            Stage Complete!')
        print(bubble.renderText('       Stage Complete      '))
        print()
        if self.hero.weapon is not None:
            print(f'    Current weapon: {self.hero.weapon.name} +{self.hero.weapon.damage} damage       ')
            print()
        self.hero.display_health()
        self.enemy.display_health()
        if self.loss == True:
            self.loss = False
            self.hero.max_health = 100
        

    def start_game(self):
        while True:
            os.system('clear')
            print()
            print(custom_fig.renderText('Mystical Realms'))
            # print()
            # if self.enemy_damage_increase != 0:
            #     print(f'     Enemy damage increased by: +{self.enemy_damage_increase}')
            #     print()
            # print('                  Press Enter to Start!       ')
            # input()
            if self.stage == 1:
                if cutie.prompt_yes_or_no('Start New Game', default_is_yes=True):
                    self.battle()
                else:
                    break
            else:
                if cutie.prompt_yes_or_no('Continue to next stage?', default_is_yes=True):
                    self.battle()
                else:
                    break

            print()
            # play_again = input('    Do you want to play again? (yes/no): ')
            if cutie.prompt_yes_or_no('     Do you want to play again?', default_is_yes=True):
                os.system('clear')
                self.hero.reset()
                self.enemy.reset()
                random_enemy = Random_Enemy()
                new_enemy = random_enemy.get_enemy()
                next_enemy = Enemy(name=new_enemy.name, health=new_enemy.health + self.enemy_health_increase, damage=new_enemy.damage + self.enemy_damage_increase)
                self.enemy = next_enemy
            else:
                break

            # if play_again.lower() != 'yes':
            #     break
            # else:
            #     os.system('clear')
            #     self.hero.reset()
            #     self.enemy.reset()
            #     random_enemy = Random_Enemy()
            #     new_enemy = random_enemy.get_enemy()
            #     next_enemy = Enemy(name=new_enemy.name, health=new_enemy.health, damage=new_enemy.damage)
            #     self.enemy = next_enemy 

                

enemies = Random_Enemy()
print({enemies.get_enemy()})
get_enemy = enemies.get_enemy()
print(get_enemy.name)

hero = Hero(name='Hero', health=100, damage=25)
# enemy = Enemy(name='Enemy', health=100, damage=25)
enemy = Enemy(name=get_enemy.name, health=get_enemy.health, damage=get_enemy.damage)

game = GameLoop(hero, enemy)
game.start_game()
