from flask import Flask, render_template, jsonify, request
from game.character import Hero, Enemy
from game.enemy import Random_Enemy
from game.main import GameLoop
from game.loot import Loot
import random

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
    data = request.get_json()
    action = data.get('action')
    message = ""
    
    if action == 'start_battle':
        # Reset hero to initial state when starting a new battle
        game.stage = 1
        game.enemy_damage_increase = 0
        game.enemy_health_increase = 0
        game.hero = Hero(name='Hero', health=100, damage=25)
        game.flee_attempts = 2  # Reset flee attempts
        
        random_enemy = Random_Enemy()
        new_enemy = random_enemy.get_enemy(game.stage)
        game.enemy = Enemy(name=new_enemy.name, 
                         health=new_enemy.health, 
                         damage=new_enemy.damage)
        return jsonify({
            'message': f"Battle started against {game.enemy.name}!",
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'battle_active': True,
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'max_health': game.enemy.health
            },
            'hero_stats': {
                'weapon': "None",  # Reset weapon
                'weapon_damage': 0,
                'base_damage': 25,  # Reset to base damage
                'health_bonus': 0   # Reset health bonus
            },
            'clear_text': True  # Add this to clear text at start
        })
    
    elif action == 'attack':
        # Player's turn first
        hero_damage = game.hero.attack()
        game.enemy.take_damage(hero_damage)
        
        # Include weapon information in damage message
        if game.hero.weapon:
            message = f"You deal {hero_damage} damage with {game.hero.weapon.name}."
        else:
            message = f"You deal {hero_damage} damage."
        
        # Check if enemy died from player's attack
        if not game.enemy.is_alive():
            message += "\nEnemy has been defeated! 🎉"
            
            # Increment stage and handle stage-based bonuses
            game.increment_stage()
            
            # Handle enemy stat increases based on stage
            if game.stage % 2 == 1:
                game.enemy_damage_increase += 5
                message += "\nEnemy has gained +5 damage!"
            if game.stage % 5 == 0:
                game.enemy_health_increase += 15
                message += "\nEnemy has gained +15 health!"
            
            # Generate loot
            current_loot = Loot().get_random_loot()
            message += f"\nYou found a {current_loot.name}! (+{current_loot.damage} damage)"
            
            return jsonify({
                'message': message,
                'hero_health': game.hero.health,
                'hero_max_health': game.hero.max_health,
                'enemy_health': 0,
                'enemy_max_health': game.enemy.max_health,
                'enemy_name': game.enemy.name,
                'battle_active': False,
                'victory': True,
                'show_loot_choice': True,
                'stage': game.stage,
                'hero_stats': {
                    'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                    'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                    'base_damage': game.hero.damage,
                    'health_bonus': max(0, game.hero.max_health - 100)
                }
            })
        
        # Enemy's turn only if they survived the hero's attack
        enemy_damage = game.enemy.attack()
        game.hero.take_damage(enemy_damage)
        message += f"\n{game.enemy.name} deals {enemy_damage} damage."
        
        # Check if hero died
        if not game.hero.is_alive():
            message += "\nYou have been defeated! 💀"
            # Reset game state
            game.stage = 1
            game.enemy_damage_increase = 0
            game.enemy_health_increase = 0
            game.hero = Hero(name='Hero', health=100, damage=25)  # Reset hero to initial state
            
            return jsonify({
                'message': message,
                'hero_health': 0,  # Set health to 0 for display
                'hero_max_health': 100,
                'enemy_health': game.enemy.health,
                'enemy_max_health': game.enemy.max_health,
                'enemy_name': game.enemy.name,
                'battle_active': False,
                'game_over': True,  # Add game_over state
                'victory': False,
                'hero_stats': {
                    'weapon': "None",  # Reset weapon
                    'weapon_damage': 0,
                    'base_damage': 25,
                    'health_bonus': 0
                },
                'stage': 1  # Reset stage
            })
        
        # Both survived - continue battle
        message += f"\n{game.enemy.name} deals {enemy_damage} damage."
        return jsonify({
            'message': message,
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'battle_active': True,
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'max_health': game.enemy.max_health
            },
            'enemy_damage_increase': game.enemy_damage_increase,
            'enemy_health_increase': game.enemy_health_increase,
            'game_over': False,
            'victory': False
        })

    elif action == 'flee':
        if game.flee_attempts <= 0:
            message = "No more flee attempts remaining!"
            return jsonify({'message': message, 'battle_active': True})

        game.flee_attempts -= 1
        
        # 30% chance to lose weapon when fleeing
        weapon_lost = False
        if game.hero.weapon and random.random() < 0.3:
            lost_weapon = game.hero.weapon.name
            game.hero.weapon = None  # Remove weapon
            weapon_lost = True
            message = f"You fled from battle! Your {lost_weapon} was lost in the escape!"
        else:
            message = f"You fled from battle! ({game.flee_attempts} flee attempts remaining)"
        
        # Decrease stage by 1 (minimum 1)
        if game.stage > 1:
            game.stage -= 1
            
        # Get new enemy for previous stage
        random_enemy = Random_Enemy()
        new_enemy = random_enemy.get_enemy(game.stage)
        game.enemy = Enemy(
            name=new_enemy.name,
            health=new_enemy.health + game.enemy_health_increase,
            damage=new_enemy.damage + game.enemy_damage_increase
        )
        
        return jsonify({
            'message': message,
            'battle_active': True,
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'max_health': game.enemy.max_health
            },
            'hero_stats': {
                'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                'base_damage': game.hero.damage,
                'health_bonus': max(0, game.hero.max_health - 100)
            },
            'stage': game.stage,
            'clear_text': True
        })

    elif action == 'loot_choice':
        if current_loot is None:
            return jsonify({
                'message': "No loot available to equip",
                'battle_active': False
            })
            
        choice = data.get('loot_choice')
        if choice == 'accept':
            game.hero.equip(current_loot)
            message = f"You equipped the {current_loot.name}!"
        else:
            message = "You declined the weapon."
            
        # Clear the current loot after handling choice
        current_loot = None
        
        return jsonify({
            'message': message,
            'hero_stats': {
                'weapon': game.hero.weapon.name if game.hero.weapon else "None",
                'weapon_damage': game.hero.weapon.damage if game.hero.weapon else 0,
                'base_damage': game.hero.damage,
                'health_bonus': max(0, game.hero.max_health - 100)
            },
            'battle_active': False,
            'hero_health': game.hero.health,
            'hero_max_health': game.hero.max_health,
            'stage': game.stage
        })

    elif action == 'next_stage':
        # Properly restore hero's health to max_health
        game.hero.restore_health()
        
        # Get new enemy with proper stage scaling
        random_enemy = Random_Enemy()
        new_enemy = random_enemy.get_enemy(game.stage)
        
        # Apply stage-based enemy stat increases
        game.enemy = Enemy(
            name=new_enemy.name,
            health=new_enemy.health + game.enemy_health_increase,
            damage=new_enemy.damage + game.enemy_damage_increase
        )
        
        return jsonify({
            'message': f"Starting battle against {game.enemy.name}!",
            'hero_health': game.hero.max_health,
            'hero_max_health': game.hero.max_health,
            'enemy_health': game.enemy.health,
            'enemy_max_health': game.enemy.max_health,
            'enemy_name': game.enemy.name,
            'battle_active': True,
            'enemy_stats': {
                'name': game.enemy.name,
                'damage': game.enemy.damage,
                'max_health': game.enemy.max_health
            },
            'enemy_damage_increase': game.enemy_damage_increase,
            'enemy_health_increase': game.enemy_health_increase,
            'game_over': False,
            'victory': False,
            'clear_text': True  # Add this to clear text for new stage
        })


if __name__ == '__main__':
    app.run(debug=True)
