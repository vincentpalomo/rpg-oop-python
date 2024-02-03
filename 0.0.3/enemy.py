import random
from character import Enemy, enemies, easy_enemies, medium_enemies, hard_enemies, elite_enemies, bosses

class Random_Enemy:
    def __init__(self) -> None:
        self.enemies = enemies

    def get_enemy(self, stage):

        if not self.enemies:
            return None
        
        if stage < 10:
            self.enemies = easy_enemies
        elif stage == 10:
            self.enemies = bosses
        elif stage > 10 and stage < 20:
            self.enemies = medium_enemies
        elif stage == 20:
            self.enemies = bosses
        elif stage > 20 and stage < 30:
            self.enemies = hard_enemies
        elif stage == 30:
            self.enemies = bosses
        elif stage > 30 and stage < 40:
            self.enemies = elite_enemies
        elif stage == 40:
            self. enemies = bosses

        random_enemy = random.choice(self.enemies)
        return Enemy(
                name=random_enemy.name,
                health=random_enemy.health,
                damage=random_enemy.damage
                )
