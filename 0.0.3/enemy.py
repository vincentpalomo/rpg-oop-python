import random
from character import Enemy, enemies

class Random_Enemy:
    def __init__(self) -> None:
        self.enemies = enemies

    def get_enemy(self):
        if not self.enemies:
            return None

        random_enemy = random.choice(enemies)
        return Enemy(
                name=random_enemy.name,
                health=random_enemy.health,
                damage=random_enemy.damage
                )
