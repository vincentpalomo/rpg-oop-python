# --------- imports ----------------
import os
from character import Hero, Enemy
from weapon import short_bow, morning_star

# ----------- setup --------------------

hero = Hero(name='jinx', health=100)
hero.equip(morning_star)
enemy = Enemy(name='doo', health=120, weapon=short_bow)


# ---------- game loop ----------------
while True:
  os.system('clear')

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
elif enemy.is_dead():
  print(f'{hero.name} has defeated {enemy.name}! ⚔')
else:
  print('it\'s a draw!')