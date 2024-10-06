import random
from character import Enemy, enemies, easy_enemies, medium_enemies, hard_enemies, elite_enemies, mystic_enemies, spectral_enemies, bosses

class Random_Enemy:
    def __init__(self) -> None:
        self.enemies = enemies

    def get_enemy(self, stage):

        if not self.enemies:
            return None

        if stage % 10 == 0:
            self.enemies = bosses
        elif stage < 10:
            self.enemies = easy_enemies
        elif 10 < stage < 20:
            self.enemies = medium_enemies
        elif 20 < stage < 30:
            self.enemies = hard_enemies
        elif 30 < stage < 40:
            self.enemies = elite_enemies
        elif 40 < stage < 50:
            self.enemies = mystic_enemies
        elif 50 < stage < 60:
            self.enemies = spectral_enemies
        elif stage >= 60:
            enemy_tiers = [easy_enemies, medium_enemies, hard_enemies, elite_enemies, mystic_enemies, spectral_enemies]
            self.enemies = enemy_tiers[(stage // 10) % len(enemy_tiers)]

        random_enemy = random.choice(self.enemies)
        return Enemy(
                name=random_enemy.name,
                health=random_enemy.health,
                damage=random_enemy.damage
                )
