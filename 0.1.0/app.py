from flask import Flask, render_template, jsonify, request
from game.character import Hero, Enemy
from game.enemy import Random_Enemy
from game.main import GameLoop
from game.loot import Loot

app = Flask(__name__)

# Store current loot globally
current_loot = None

# Initialize game state
enemies = Random_Enemy()
get_enemy = enemies.get_enemy(1)
hero = Hero(name='Hero', health=100, damage=25)
enemy = Enemy(name=get_enemy.name, health=get_enemy.health,
              damage=get_enemy.damage)
game = GameLoop(hero, enemy)


@app.route('/')
def index():
    print("Index route accessed")
    return render_template('index.html')


@app.route('/api/action', methods=['POST'])
def handle_action():
    global current_loot
    action = request.json.get('action')
    loot_choice = request.json.get('loot_choice')

    if action == 'flee':
        # Reset everything to initial state
        game.stage = 1
        game.enemy_damage_increase = 0
        game.enemy_health_increase = 0
        
        # Complete hero reset
        game.hero = Hero(name='Hero', health=100, damage=25)  # Create fresh hero
        game.hero.max_health = 100  # Explicitly reset max health
        game.hero.health = game.hero.max_health
        game.hero.weapon = None
        
        # Reset enemy health but keep same enemy
        game.enemy.health = game.enemy.max_health
        
        current_loot = None

        return jsonify({
            'message': "You fled from battle! All progress has been reset to Stage 1.",
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,  # This will be 100 now
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'stage': game.stage,
            'battle_active': False,
            'hero_stats': {
                'weapon': "None",
                'weapon_damage': 0,
                'base_damage': game.hero.damage,
                'health_bonus': 0  # Explicitly show 0 health bonus
            },
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'health': game.enemy.health,
                'max_health': game.enemy.max_health
            }
        })

    elif action == 'start_battle':
        # Create new enemy first, then use it consistently
        get_enemy = enemies.get_enemy(game.stage)
        game.enemy = Enemy(
            name=get_enemy.name,
            health=get_enemy.health + game.enemy_health_increase,
            damage=get_enemy.damage + game.enemy_damage_increase
        )

        # Reset hero health
        game.hero.health = game.hero.max_health

        # Clear text for boss battles
        is_boss = game.stage % 10 == 0
        message = "BOSS BATTLE!" if is_boss else f'Battle started against {
            game.enemy.name}!'

        return jsonify({
            'message': message,
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'stage': game.stage,
            'battle_active': True,
            'clear_text': is_boss,
            'hero_stats': {
                'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                'base_damage': game.hero.damage,
                'health_bonus': game.hero.max_health - 100
            },
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'health': game.enemy.health,
                'max_health': game.enemy.max_health
            }
        })

    elif action == 'attack':
        hero_damage = game.hero.attack()
        enemy_damage = game.enemy.attack()

        game.enemy.take_damage(hero_damage)
        game.hero.take_damage(enemy_damage)

        message = f"You deal {hero_damage} damage. Enemy deals {
            enemy_damage} damage."

        if game.hero.health <= 0:
            message += f"\nYou have been defeated! Game Over!"
            # Complete reset of game state
            game.stage = 1
            game.enemy_damage_increase = 0
            game.enemy_health_increase = 0

            # Create fresh hero with base stats
            game.hero = Hero(name='Hero', health=100, damage=25)
            game.hero.max_health = 100  # Explicitly reset max health
            game.hero.health = game.hero.max_health
            game.hero.weapon = None

            return jsonify({
                'message': message,
                'hero_health': 0,  # Show 0 health for defeat
                'hero_max_health': 100,  # Reset to base max health
                'enemy_health': game.enemy.health,  # Keep current enemy health
                'enemy_max_health': game.enemy.max_health,
                'enemy_name': game.enemy.name,
                'stage': game.stage,
                'battle_active': False,
                'hero_stats': {
                    'weapon': "None",
                    'weapon_damage': 0,
                    'base_damage': 25,
                    'health_bonus': 0  # Explicitly show 0 health bonus
                },
                'enemy_stats': {
                    'name': game.enemy.name,
                    'damage': game.enemy.damage,
                    'health': game.enemy.health,
                    'max_health': game.enemy.max_health
                }
            })

        if game.enemy.health <= 0:
            message += f"\n\n{game.enemy.name} has been defeated!"

            # Increment stage before getting loot
            game.stage += 1
            message += f"\nAdvancing to Stage {game.stage}!"

            # Apply stage bonuses
            if (game.stage - 1) % 2 == 1:
                game.enemy_damage_increase += 5
                message += "\nEnemy damage increased by 5!"
            if (game.stage - 1) % 5 == 0:
                game.enemy_health_increase += 15
                message += "\nEnemy health increased by 15!"
            if (game.stage - 1) % 10 == 0:
                game.hero.increase_damage()
                message += "\nHero damage increased!"

            game.hero.increase_health()

            # Get loot and store it
            loot = Loot()
            current_loot = loot.get_random_loot()
            message += f"\nYou obtained a(n) {current_loot.name}! (+{
                current_loot.damage} damage)"

            return jsonify({
                'message': message,
                'hero_health': game.hero.health,
                'hero_max_health': game.hero.max_health,
                'enemy_health': game.enemy.health,
                'enemy_max_health': game.enemy.max_health,
                'enemy_name': game.enemy.name,
                'stage': game.stage,
                'show_loot_choice': True,
                'clear_text': game.stage % 10 == 0,  # Clear text if next stage is boss
                'hero_stats': {
                    'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                    'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                    'base_damage': game.hero.damage,
                    'health_bonus': game.hero.max_health - 100
                },
                'enemy_stats': {
                    'name': game.enemy.name,
                    'damage': game.enemy.damage,
                    'health': game.enemy.health,
                    'max_health': game.enemy.max_health
                }
            })

        # Return for normal attack
        return jsonify({
            'message': message,
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'stage': game.stage,
            'battle_active': True,
            'hero_stats': {
                'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                'base_damage': game.hero.damage,
                'health_bonus': game.hero.max_health - 100
            },
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'health': game.enemy.health,
                'max_health': game.enemy.max_health
            }
        })

    elif action == 'loot_choice':
        if loot_choice == 'accept' and current_loot:
            game.hero.equip(current_loot)
            message = f"You equipped the {current_loot.name}!"
        else:
            message = "You declined the weapon."

        # Reset hero health to max before new enemy
        game.hero.health = game.hero.max_health

        # Create new enemy
        get_enemy = enemies.get_enemy(game.stage)
        game.enemy = Enemy(
            name=get_enemy.name,
            health=get_enemy.health + game.enemy_health_increase,
            damage=get_enemy.damage + game.enemy_damage_increase
        )

        message += f"\nA new enemy appears: {game.enemy.name}!"
        current_loot = None  # Clear the stored loot

        return jsonify({
            'message': message,
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'stage': game.stage,
            'battle_active': True,
            'hero_stats': {
                'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                'base_damage': game.hero.damage,
                'health_bonus': game.hero.max_health - 100
            },
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'health': game.enemy.health,
                'max_health': game.enemy.max_health
            }
        })


if __name__ == '__main__':
    app.run(debug=True)
