class Weapon:
  def __init__(self, name: str, weapon_type: str, damage: int) -> None:
    self.name = name
    self.weapon_type = weapon_type
    self.damage = damage

# swords
iron_sword = Weapon(name='iron sword', weapon_type='sword', damage=15)
bronze_sword = Weapon(name='bronze sword', weapon_type='sword', damage=25)
silver_sword = Weapon(name='silver sword', weapon_type='sword', damage=45)
great_sword = Weapon(name='great sword', weapon_type='sword', damage=50)
kingsblade = Weapon(name='kingsblade', weapon_type='sword', damage=65)
shadow_blade = Weapon(name='shadow blade', weapon_type='sword', damage=70)
death_daggers = Weapon(name='death daggers', weapon_type='sword', damage=75)
sun_stealer = Weapon(name='sun stealer', weapon_type='sword', damage=75)

# bows
short_bow = Weapon(name='short bow', weapon_type='ranged', damage=10)
long_bow = Weapon(name='long bow', weapon_type='ranged', damage=20)
recurve_bow = Weapon(name='recurve bow', weapon_type='ranged', damage=35)
great_bow = Weapon(name='great bow', weapon_type='ranged', damage=40)
master_bow = Weapon(name='master bow', weapon_type='ranged', damage=60)
elven_bow = Weapon(name='evlen bow', weapon_type='ranged', damage=80)
star_shatter = Weapon(name='star shatter', weapon_type='ranged', damage=125)

# blunt
fists = Weapon(name='iron fists', weapon_type='blunt', damage=5)
bronze_hammer = Weapon(name='bronze hammer', weapon_type='blunt', damage=15)
morning_star = Weapon(name='morning star', weapon_type='blunt', damage=40)
forged_steel_hammer = Weapon(name='forged steel hammer', weapon_type='blunt', damage=55)
moonlight_hammer = Weapon(name='moonlight hammer', weapon_type='blunt', damage=75)
jupiters_fist = Weapon(name='jupiters fist', weapon_type='blunt', damage=95)
queens_flail = Weapon(name='queens flail', weapon_type='blunt', damage=100)

# admin
one_tap = Weapon(name='one tap', weapon_type='admin', damage=10000)

get_weapons = [one_tap, iron_sword, bronze_sword, silver_sword, great_sword, kingsblade, great_bow, short_bow, long_bow, recurve_bow, fists, bronze_hammer, morning_star, forged_steel_hammer, moonlight_hammer, shadow_blade, death_daggers, 
               sun_stealer, elven_bow, star_shatter, jupiters_fist, queens_flail]
