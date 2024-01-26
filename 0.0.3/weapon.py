class Weapon:
  def __init__(self, name: str, weapon_type: str, damage: int) -> None:
    self.name = name
    self.weapon_type = weapon_type
    self.damage = damage

# swords
iron_sword = Weapon(name='iron sword', weapon_type='sword', damage=15)
bronze_sword = Weapon(name='bronze sword', weapon_type='sword', damage=25)
silver_sword = Weapon(name='silver sword', weapon_type='sword', damage=45)

# bows
short_bow = Weapon(name='short bow', weapon_type='ranged', damage=10)
long_bow = Weapon(name='long bow', weapon_type='ranged', damage=20)
recurve_bow = Weapon(name='recurve bow', weapon_type='ranged', damage=35)

# blunt
fists = Weapon(name='iron fists', weapon_type='blunt', damage=5)
bronze_hammer = Weapon(name='bronze hammer', weapon_type='blunt', damage=15)
morning_star = Weapon(name='morning star', weapon_type='blunt', damage=40)

get_weapons = [iron_sword, bronze_sword, silver_sword,short_bow, long_bow, recurve_bow, fists, bronze_hammer, morning_star]