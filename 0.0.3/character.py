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
        else:
            base_damage = self.damage
        is_critical = random.random() < 0.1

        if is_critical:
            print(f'             !CRITICAL HIT!          ')
            print(f'        {self.name} gained extra damage!')
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
        remaining_health = int((self.health / self.max_health) * bar_length)
        health_bar = '|' + '█' * remaining_health + \
            '-' * (bar_length - remaining_health) + '|'
        print(f'    {self.name}`s HP:')
        print(f'    {health_bar} {self.health}/{self.max_health}')

    def increase_health(self):
        self.max_health += 5
        print()
        print(f'    You have gained +5 health')

    def increase_damage(self):
        self.damage += 10
        print(f'    You have gained +10 damage')

    def reset(self) -> None:
        self.health = self.max_health


class Hero(Character):
    def __init__(self, name, health, damage, weapon=None) -> None:
        super().__init__(name, health, damage, weapon)

    def equip(self, weapon) -> None:
        self.weapon = weapon
        print()
        print(f'        {self.name} equipped a(n) {self.weapon.name}!')

    def player_down(self) -> None:
        self.weapon = None
        self.damage = 25

    def reset(self):
        super().reset()


class Enemy(Character):
    def __init__(self, name, health, damage, weapon=None) -> None:
        super().__init__(name, health, damage, weapon)
    
    def increase_damage(self) -> None:
        self.damage += 5
        print()
        print(f'    {"~" * 10} Enemy damage increased by {5} {"~" * 10}')
    
    def reset_damage(self) -> None:
        self.damage = 25


# enemies
orc = Enemy(name='Orc', health=70, damage=10)
goblin = Enemy(name='Goblin', health=75, damage=15)
troll = Enemy(name='Troll', health=80, damage=20)
dark_elf = Enemy(name='Dark Elf', health=110, damage=30)
theif = Enemy(name='Theif', health=100, damage=25)
warlock = Enemy(name='Warlock', health=100, damage=35)
barbarian = Enemy(name='Barbarian', health=150, damage=40)
death_knight = Enemy(name='Death Knight', health=120, damage=45)
sun_worshiper = Enemy(name='Sun Worshiper', health=125, damage=50)
undead_rogue = Enemy(name='Undead Rogue', health=95, damage=25)

# boss
hell_hound = Enemy(name='Hell Hound', health=200, damage=30)
ancient_guard = Enemy(name='Ancient Guard', health=250, damage=25)
mystic_lord = Enemy(name='Mystic Lord', health=300, damage=35)

enemies = [goblin, dark_elf, theif, warlock, barbarian, orc, death_knight, troll, sun_worshiper, undead_rogue]

easy_enemies = [goblin, orc, troll, theif]
medium_enemies = [dark_elf, warlock, undead_rogue]
hard_enemies = [barbarian, death_knight, sun_worshiper]

bosses = [hell_hound, ancient_guard, mystic_lord]