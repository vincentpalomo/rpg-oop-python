import random


class Character:
    def __init__(self, name, health, damage, weapon=None) -> None:
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.weapon = weapon

    def attack(self) -> None:
        if self.weapon != None:
            base_damage = self.damage + self.weapon.damage
            # print(f'Weapon Bonus Damage {base_damage}')
        else:
            base_damage = self.damage
            # print(f'Base Damage {base_damage}')
        is_critical = random.random() < 0.1

        if is_critical:
            print(f'!CRITICAL HIT!')
            print(f'{self.name} gained extra damage!')
            print()

            return int(base_damage * 1.5)
        else:
            return random.randint(1, base_damage)

    def take_damage(self, damage) -> None:
        self.health -= damage

        if self.health < 0:
            self.health = 0

    def is_alive(self) -> None:
        return self.health > 0

    def display_health(self):
        bar_length = 30
        remaining_health = int((self.health / 100) * bar_length)
        health_bar = '|' + '█' * remaining_health + \
            '-' * (bar_length - remaining_health) + '|'
        print(f'{self.name}`s HP:')
        print(f'{health_bar} {self.health}/{self.max_health}')

    def reset(self) -> None:
        self.health = self.max_health


class Hero(Character):
    def __init__(self, name, health, damage, weapon=None) -> None:
        super().__init__(name, health, damage, weapon)

    def equip(self, weapon) -> None:
        self.weapon = weapon
        print()
        print(f'{self.name} equipped a(n) {self.weapon.name}!')

    def player_down(self) -> None:
        self.weapon = None

    def reset(self):
        super().reset()


class Enemy(Character):
    def __init__(self, name, health, damage, weapon=None) -> None:
        super().__init__(name, health, damage, weapon)
    
    def increase_damage(self) -> None:
        self.damage += 5
        print(f'Enemy damage increased by {5}')
