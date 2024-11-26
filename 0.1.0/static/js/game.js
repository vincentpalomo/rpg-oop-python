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

  if (!output || !heroStats || !enemyStats) {
    console.error('Could not find required DOM elements');
    return;
  }

  // Clear text if it's a boss battle
  if (state.clear_text) {
    output.innerHTML = '';
  }

  const timestamp = new Date().toLocaleTimeString();

  // Handle message display
  if (state.message) {
    const messageLines = state.message.split('\n').filter((line) => line); // Remove empty lines
    const formattedMessage = messageLines
      .map((line, index) => {
        if (index === 0) {
          return `<p>[${timestamp}] ${line}</p>`;
        }
        return `<p>${line}</p>`;
      })
      .join('');

    output.innerHTML += formattedMessage;
  }

  // Update health displays with health bars
  if (state.hero_health !== undefined) {
    const heroHealthBar = createHealthBar(state.hero_health, state.hero_max_health);
    heroStats.innerHTML = `
        <div class="health-display">
            ${heroHealthBar}
            <div>Hero Health: ${Math.max(0, state.hero_health)}/${state.hero_max_health}</div>
        </div>`;
  }

  if (state.enemy_health !== undefined) {
    const enemyHealthBar = createHealthBar(state.enemy_health, state.enemy_max_health);
    enemyStats.innerHTML = `
        <div class="health-display">
            ${enemyHealthBar}
            <div>${state.enemy_name}'s Health: ${Math.max(0, state.enemy_health)}/${state.enemy_max_health}</div>
        </div>`;
  }

  // Update enemy stats display (without health bar)
  if (state.enemy_stats) {
    document.getElementById('enemy-name-display').innerHTML = `Name: ${state.enemy_stats.name}`;
    document.getElementById('enemy-damage-display').innerHTML = `Damage: ${state.enemy_stats.damage}`;
    document.getElementById('enemy-health-display').innerHTML = `Health: ${state.enemy_stats.max_health}`;
  }

  // Update stats
  if (state.stage !== undefined) {
    const stageDisplay = document.getElementById('stage-display');
    if (stageDisplay) {
      stageDisplay.innerHTML = `Stage: ${state.stage}`;
    }
  }

  // Update hero stats
  if (state.hero_stats) {
    document.getElementById('weapon-equipped').innerHTML = `Weapon: ${state.hero_stats.weapon}`;
    document.getElementById('weapon-damage').innerHTML = `Weapon Damage: +${state.hero_stats.weapon_damage}`;
    document.getElementById('base-damage').innerHTML = `Base Damage: ${state.hero_stats.base_damage}`;
    document.getElementById('health-bonus').innerHTML = `Health Bonus: +${state.hero_stats.health_bonus}`;
  }

  // Handle battle state and button enabling
  if (state.battle_active !== undefined) {
    battleActive = state.battle_active;
    startBattleButton.disabled = battleActive;
    
    // Enable combat buttons only if battle is active
    attackButton.disabled = !battleActive;
    autoAttackButton.disabled = !battleActive;
    fleeButton.disabled = !battleActive;
    
    if (!battleActive) {
      stopAutoAttack();  // Stop auto attack if it's running
    }
  }

  // Handle loot choice buttons
  if (state.show_loot_choice) {
    attackButton.disabled = true;
    autoAttackButton.disabled = true;
    fleeButton.disabled = true;
    stopAutoAttack();  // Stop auto attack if it's running
    acceptLoot.disabled = false;
    declineLoot.disabled = false;
  } else if (battleActive) {  // Only enable combat buttons if battle is active
    attackButton.disabled = false;
    autoAttackButton.disabled = false;
    fleeButton.disabled = false;
    acceptLoot.disabled = true;
    declineLoot.disabled = true;
  }

  // Keep battle stats visible always after first shown
  if (state.hero_health !== undefined) {
    document.getElementById('hero-stats').style.visibility = 'visible';
  }
  if (state.enemy_health !== undefined) {
    document.getElementById('enemy-stats').style.visibility = 'visible';
  }

  // Scroll to bottom
  output.scrollTop = output.scrollHeight;
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

    // Reset button states
    document.getElementById('attack').disabled = true;
    document.getElementById('start-battle').disabled = false;
    battleActive = false;
  } catch (error) {
    console.error('Error:', error);
  }
}

function toggleAutoAttack() {
  const autoAttackButton = document.getElementById('auto-attack');
  if (!isAutoAttacking) {
    isAutoAttacking = true;
    autoAttackButton.textContent = 'Stop Auto';
    autoAttackButton.style.backgroundColor = '#e74c3c';
    autoAttackInterval = setInterval(attack, 1000); // Attack every second
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
