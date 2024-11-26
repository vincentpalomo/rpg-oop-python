let battleActive = false;
let autoAttackInterval = null;
let isAutoAttacking = false;

async function startBattle() {
  if (battleActive) return;

  try {
    const response = await fetch('/api/action', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'start_battle',
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    battleActive = true;
    updateGameState(result);

    // Enable attack button and disable start battle
    document.getElementById('attack').disabled = false;
    document.getElementById('start-battle').disabled = true;
  } catch (error) {
    console.error('Error:', error);
  }
}

async function handleLoot(choice) {
  const acceptLoot = document.getElementById('accept-loot');
  const declineLoot = document.getElementById('decline-loot');
  
  // Disable buttons immediately after choice
  acceptLoot.disabled = true;
  declineLoot.disabled = true;
  
  try {
    const response = await fetch('/api/action', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'loot_choice',
        loot_choice: choice,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    updateGameState(result);
    
    // Automatically start next stage after loot decision
    nextStage();
  } catch (error) {
    console.error('Error:', error);
  }
}

function createHealthBar(current, max, width = 20) {
  const percentage = Math.max(0, current) / max;
  const filledBlocks = Math.round(percentage * width);
  const emptyBlocks = width - filledBlocks;

  return `<div class="health-bar">
    <div class="bar-container">
      <span class="empty" style="color: #bdc3c7">${'░'.repeat(width)}</span>
      <span class="filled" style="color: ${percentage > 0.5 ? '#2ecc71' : percentage > 0.25 ? '#f1c40f' : '#e74c3c'}">${'█'.repeat(
    filledBlocks
  )}</span>
    </div>
  </div>`;
}

function updateGameState(state) {
  console.log('Updating game state:', state);
  const output = document.getElementById('game-output');
  const heroStats = document.getElementById('hero-stats');
  const enemyStats = document.getElementById('enemy-stats');
  const acceptLoot = document.getElementById('accept-loot');
  const declineLoot = document.getElementById('decline-loot');
  const attackButton = document.getElementById('attack');
  const autoAttackButton = document.getElementById('auto-attack');
  const fleeButton = document.getElementById('flee');
  const startBattleButton = document.getElementById('start-battle');
  const stageDisplay = document.getElementById('stage-display');

  // Only clear the output if explicitly told to or starting new stage
  if (state.clear_text) {
    output.innerHTML = '';
  }

  // Handle message display with timestamps
  if (state.message) {
    const timestamp = new Date().toLocaleTimeString();
    const messages = state.message.split('\n').filter(msg => msg.trim() !== ''); // Remove empty messages
    
    // Create new formatted messages
    const formattedMessages = messages.map(msg => {
      // Only add timestamp to damage messages
      if (msg.includes('deal') && msg.includes('damage')) {
        return `[${timestamp}] ${msg}`;
      }
      return msg;
    });
    
    // Only clear text if explicitly told to
    if (state.clear_text) {
      output.innerHTML = '';
    }
    
    // Add new messages
    const newMessageHTML = formattedMessages
      .filter((msg, index, self) => self.indexOf(msg) === index) // Remove duplicates
      .map(msg => `<p>${msg}</p>`)
      .join('');
      
    output.innerHTML += newMessageHTML;
    
    // Scroll to bottom
    output.scrollTop = output.scrollHeight;
  }

  // Update health displays
  if (state.hero_health !== undefined && state.hero_max_health !== undefined) {
    const heroHealthBar = createHealthBar(
      state.game_over ? 0 : state.hero_health, 
      state.hero_max_health
    );
    heroStats.innerHTML = `
        <div class="health-display">
            ${heroHealthBar}
            <div>Hero Health: ${Math.max(0, state.hero_health)}/${state.hero_max_health}</div>
        </div>`;
    heroStats.style.visibility = 'visible';
  }

  if (state.enemy_health !== undefined && state.enemy_max_health !== undefined) {
    const enemyHealthBar = createHealthBar(state.enemy_health, state.enemy_max_health);
    enemyStats.innerHTML = `
        <div class="health-display">
            ${enemyHealthBar}
            <div>${state.enemy_name}'s Health: ${Math.max(0, state.enemy_health)}/${state.enemy_max_health}</div>
        </div>`;
    enemyStats.style.visibility = 'visible';
  }

  // Update enemy stats display with bonuses
  if (state.enemy_stats) {
    const healthBonus = state.enemy_health_increase || 0;
    const damageBonus = state.enemy_damage_increase || 0;
    
    document.getElementById('enemy-name-display').innerHTML = `Name: ${state.enemy_stats.name}`;
    document.getElementById('enemy-damage-display').innerHTML = 
        `Damage: ${state.enemy_stats.damage}${damageBonus ? ` (+${damageBonus})` : ''}`;
    document.getElementById('enemy-health-display').innerHTML = 
        `Health: ${state.enemy_stats.max_health}${healthBonus ? ` (+${healthBonus})` : ''}`;
  }

  // Update stage display
  if (state.stage !== undefined) {
    stageDisplay.innerHTML = `Stage: ${state.stage}`;
  }

  // Update hero stats
  if (state.hero_stats) {
    document.getElementById('weapon-equipped').innerHTML = `Weapon: ${state.hero_stats.weapon}`;
    document.getElementById('weapon-damage').innerHTML = `Weapon Damage: +${state.hero_stats.weapon_damage}`;
    document.getElementById('base-damage').innerHTML = `Base Damage: ${state.hero_stats.base_damage}`;
    document.getElementById('health-bonus').innerHTML = `Health Bonus: +${state.hero_stats.health_bonus}`;
  }

  // Update battle state and buttons
  battleActive = state.battle_active;

  // Handle button states based on game state
  if (state.game_over) {
    // When game is over (player defeated), disable combat buttons and enable start battle
    attackButton.disabled = true;
    autoAttackButton.disabled = true;
    fleeButton.disabled = true;
    acceptLoot.disabled = true;
    declineLoot.disabled = true;
    startBattleButton.disabled = false;  // Enable start battle
  } else if (state.victory && state.show_loot_choice) {
    // During loot choice, disable combat buttons and enable loot buttons
    attackButton.disabled = true;
    autoAttackButton.disabled = true;
    fleeButton.disabled = true;
    startBattleButton.disabled = true;  // Disable start battle
    acceptLoot.disabled = false;
    declineLoot.disabled = false;
  } else if (state.battle_active) {
    // During battle, enable combat buttons and disable others
    attackButton.disabled = false;
    autoAttackButton.disabled = false;
    fleeButton.disabled = false;
    startBattleButton.disabled = true;  // Disable start battle
    acceptLoot.disabled = true;
    declineLoot.disabled = true;
  }

  // Keep battle stats visible always after first shown
  if (state.hero_health !== undefined) {
    heroStats.style.visibility = 'visible';
  }
  if (state.enemy_health !== undefined) {
    enemyStats.style.visibility = 'visible';
  }
}

async function attack() {
  if (!battleActive) {
    stopAutoAttack();
    return;
  }
  
  try {
    const response = await fetch('/api/action', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'attack',
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    updateGameState(result);
    
    // Stop auto attack if battle ends
    if (!result.battle_active) {
      stopAutoAttack();
    }
  } catch (error) {
    console.error('Error:', error);
    stopAutoAttack();
  }
}

async function fleeGame() {
  try {
    const response = await fetch('/api/action', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'flee',
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    updateGameState(result);

    // Enable battle buttons since battle is active after fleeing
    if (result.battle_active) {
      document.getElementById('attack').disabled = false;
      document.getElementById('auto-attack').disabled = false;
      document.getElementById('flee').disabled = false;
      battleActive = true;  // Make sure battleActive is set to true
    }

  } catch (error) {
    console.error('Error:', error);
  }
}

function toggleAutoAttack() {
  const autoAttackButton = document.getElementById('auto-attack');
  if (!isAutoAttacking && battleActive) {  // Check if battle is active
    isAutoAttacking = true;
    autoAttackButton.textContent = 'Stop Auto';
    autoAttackButton.style.backgroundColor = '#e74c3c';
    autoAttackInterval = setInterval(async () => {
      if (battleActive) {  // Check battle is still active before each attack
        await attack();
      } else {
        stopAutoAttack();  // Stop if battle ends
      }
    }, 1000);
  } else {
    stopAutoAttack();
  }
}

function stopAutoAttack() {
  const autoAttackButton = document.getElementById('auto-attack');
  isAutoAttacking = false;
  autoAttackButton.textContent = 'Auto Attack';
  autoAttackButton.style.backgroundColor = '';
  if (autoAttackInterval) {
    clearInterval(autoAttackInterval);
    autoAttackInterval = null;
  }
}

// When the page loads, ensure combat buttons are disabled
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('attack').disabled = true;
    document.getElementById('auto-attack').disabled = true;
    document.getElementById('flee').disabled = true;
});

// Add new function to handle next stage
async function nextStage() {
    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'next_stage',
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        battleActive = true;  // Set battle as active
        updateGameState(result);
    } catch (error) {
        console.error('Error:', error);
    }
}
