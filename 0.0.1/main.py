# --------- imports ----------------
import os
from character import Hero, Enemy
from weapon import iron_sword, bronze_sword, silver_sword, short_bow, long_bow, recurve_bow, fists, bronze_hammer, morning_star
from loot import Loot

# -------- initialize stage -------------------------------
current_stage = 1

loot_table = Loot()
loot_table.add_weapon(iron_sword)
loot_table.add_weapon(bronze_sword)
loot_table.add_weapon(silver_sword)
loot_table.add_weapon(short_bow)
loot_table.add_weapon(long_bow)
loot_table.add_weapon(recurve_bow)
loot_table.add_weapon(fists)
loot_table.add_weapon(bronze_hammer)
loot_table.add_weapon(morning_star)


hero = Hero(name='jinx', health=100, initial_weapon=iron_sword)
enemy = Enemy(name='doo', health=120, weapon=short_bow)

# --------------------- main game loop -----------------------
game_online = True

while game_online:
    
    hero.reset()
    enemy.reset()

    # ---------- game loop ----------------
    while True:
        os.system('clear')

        print(f'Stage {current_stage}')

        hero.attack(enemy)
        enemy.attack(hero)

        hero.health_bar.draw()
        enemy.health_bar.draw()

        if hero.is_dead() or enemy.is_dead():
            break

        input()

    # ---------- battle message ---------
    if hero.is_dead():
        print(f'{enemy.name} has defeated {hero.name}! 💀')
        break
    elif enemy.is_dead():
        print(f'{hero.name} has defeated {enemy.name}! ⚔')

        loot = loot_table.get_random_loot()
        if loot:
            print(f'You obtained a {loot.name}!')
            answer = input('Do you want to equip the loot? (yes/no): ')
            if answer.lower() == 'yes':
                hero.equip(loot)
                print(f'{hero.name} has equipped the {loot.name}!')
            else:
                print(f'The loot was not equipped.')
        else:
            print(f'No loot was dropped')

    answer = input('Do you want to go to the next round? (yes/no): ')
    if answer.lower() == 'no':
        game_online = False
    elif answer.lower() == 'yes':
        current_stage += 1