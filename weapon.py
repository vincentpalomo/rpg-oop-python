# ------------ class setup -----------------
class Weapon:
  def __init__(self, name: str, weapon_type: str, damage: int, value: int) -> None:
    self.name = name
    self.weapon_type = weapon_type
    self.damage = damage
    self.value = value

# ------------ object creation -------------

# swords
iron_sword = Weapon(name='iron sword', weapon_type='sword', damage=15, value=10)
bronze_sword = Weapon(name='bronze sword', weapon_type='sword', damage=25, value=15)
silver_sword = Weapon(name='silver sword', weapon_type='sword', damage=45, value=20)

# bows
short_bow = Weapon(name='short bow', weapon_type='ranged', damage=10, value=10)
long_bow = Weapon(name='long bow', weapon_type='ranged', damage=20, value=15)
recurve_bow = Weapon(name='recurve bow', weapon_type='ranged', damage=35, value=50)

# blunt
fists = Weapon(name='fists', weapon_type='blunt', damage=5, value=0)
bronze_hammer = Weapon(name='bronze hammer', weapon_type='blunt', damage=15, value=10)
morning_star = Weapon(name='morning star', weapon_type='blunt', damage=40, value=45)