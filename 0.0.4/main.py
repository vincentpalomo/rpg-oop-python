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
        self.highest_stage = 0
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

        if self.enemy_health_increase != 0:
            print(f'     Enemy health increased by: +{self.enemy_health_increase}')

        if self.hero.max_health > 100:
            print()
            print(f'     Current health boost: +{self.hero.health - 100}')

        if self.hero.damage > 25:
            print(f'     Current damage boost: +{self.hero.damage - 25}')

        print()
        # print(bubble.renderText('     Prepare for battle      '))

        if self.stage % 10 == 0:
            print(bubble.renderText('   Boss Battle     '))
        else:
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
                    print(f'    enemy has gained +15 health!')
                    self.enemy_health_increase += 15
                self.increment_stage()

                if self.stage % 10 == 0:
                    self.hero.increase_damage()

                self.hero.increase_health()
                self.highest_stage += 1
                time.sleep(3)
                
                os.system('clear')
                loot = Loot()
                get_loot = loot.get_random_loot()
                print()
                print(f'        You obtained a(n) {get_loot.name}! +{get_loot.damage} damage')
                print()
                if self.hero.weapon is not None:
                     print(f'   Current weapon equipped: {self.hero.weapon.name} +{self.hero.weapon.damage} damage')
                     print()
                
                if cutie.prompt_yes_or_no('     Do you want to equip the loot? ', char_prompt=False):
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
                print(f'    You haven fallen at stage: {self.stage}      ') 
                self.highest_stage += 1
                self.stage = 1
                self.loss = True
                self.enemy_damage_increase = 0
                self.enemy_health_increase = 0
                time.sleep(2)
                break

            print()
            # input('     Press any button to continue...')

        os.system('clear')
        print()
        # print(f'            Stage Complete!')
        if self.highest_stage <= 1:
            print(bubble.renderText(f'      Stage 1 Complete        '))
        else:
            print(bubble.renderText(f'       Stage {self.highest_stage} Complete      '))
        
        print()
        if self.hero.weapon is not None:
            print(f'    Current weapon: {self.hero.weapon.name} +{self.hero.weapon.damage} damage       ')
            print()
        self.hero.display_health()
        self.enemy.display_health()
        if self.loss == True:
            self.loss = False
            self.hero.max_health = 100
            self.highest_stage = 0
        

    def start_game(self):
        while True:
            os.system('clear')
            print()
            print(custom_fig.renderText('Mystical Realms'))

            if self.stage == 1:
                if cutie.prompt_yes_or_no('Start New Game', default_is_yes=True, char_prompt=False):
                    self.battle()
                else:
                    break
            else:
                if cutie.prompt_yes_or_no('Continue to next stage?', default_is_yes=True, char_prompt=False):
                    self.battle()
                else:
                    break

            print()

            if cutie.prompt_yes_or_no('     Do you want to play again?', default_is_yes=True, char_prompt=False):
                os.system('clear')
                self.hero.reset()
                self.enemy.reset()
                random_enemy = Random_Enemy()
                new_enemy = random_enemy.get_enemy(self.stage)
                next_enemy = Enemy(name=new_enemy.name, health=new_enemy.health + self.enemy_health_increase, damage=new_enemy.damage + self.enemy_damage_increase)
                self.enemy = next_enemy
            else:
                break
    

enemies = Random_Enemy()
get_enemy = enemies.get_enemy(1)

hero = Hero(name='Hero', health=100, damage=25)
enemy = Enemy(name=get_enemy.name, health=get_enemy.health, damage=get_enemy.damage)

game = GameLoop(hero, enemy)
game.start_game()
