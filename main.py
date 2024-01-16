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

  # print(f'Health of {hero.name}: {hero.health}')
  # print(f'Health of {enemy.name}: {enemy.health}')

  hero.health_bar.draw()
  enemy.health_bar.draw()

  input()