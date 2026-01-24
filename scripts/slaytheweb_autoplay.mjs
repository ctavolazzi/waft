import fs from 'fs'
import path from 'path'

import createNewGame from '../_external/slaytheweb/src/game/new-game.js'
import {canPlay} from '../_external/slaytheweb/src/game/conditions.js'
import {CardTargets} from '../_external/slaytheweb/src/game/cards.js'
import {getCurrRoom, isCurrRoomCompleted, isDungeonCompleted} from '../_external/slaytheweb/src/game/utils-state.js'

const args = process.argv.slice(2)
const getArg = (name, fallback) => {
	const index = args.indexOf(name)
	if (index === -1) return fallback
	const value = args[index + 1]
	return value ?? fallback
}

const maxTurns = Number(getArg('--max-turns', process.env.MAX_TURNS || 50))
const outDir =
	getArg(
		'--out-dir',
		process.env.OUT_DIR ||
			path.join(
				process.cwd(),
				'_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs',
			),
	) || '.'

const runId = `stw_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
const startedAt = new Date().toISOString()

const game = createNewGame(false)
let state = game.state

const actionsLog = []
const turnsLog = []
let roomsCleared = 0
const combatRoomTypes = new Set(['monster', 'elite', 'boss'])

const resolveTarget = (card, room) => {
	if (card.target === CardTargets.player) return 'player'
	if (card.target === CardTargets.allEnemies) return CardTargets.allEnemies
	if (card.target === CardTargets.enemy) {
		if (room?.monsters?.length) {
			const aliveIndex = room.monsters.findIndex((monster) => monster.currentHealth > 0)
			if (aliveIndex >= 0) return `enemy${aliveIndex}`
		}
		return null
	}
	return null
}

const nextMoveFromPath = (state) => {
	const curr = [state.dungeon.y, state.dungeon.x]
	const path = state.dungeon.paths?.[0] || []
	const step = path.find(
		(move) => move[0][0] === curr[0] && move[0][1] === curr[1],
	)
	if (!step) return null
	const next = step[1]
	return {x: next[1], y: next[0]}
}

for (let turn = 0; turn < maxTurns; turn++) {
	if (state.endedAt) break
	if (isDungeonCompleted(state)) break

	const room = getCurrRoom(state)

	if (room.type === 'campfire' && !room.choice) {
		state = game.actions.makeCampfireChoice(state, {choice: 'rest', reward: null})
	}
	if (!combatRoomTypes.has(room.type)) {
		if (isCurrRoomCompleted(state)) {
			const move = nextMoveFromPath(state)
			if (move) {
				state = game.actions.move(state, {move})
				roomsCleared += 1
			}
		}
		continue
	}

	let played = true
	while (played) {
		played = false
		for (const card of state.hand) {
			if (!canPlay(state, card)) continue
			const target = resolveTarget(card, room)
			if (!target) continue
			state = game.actions.playCard(state, {card, target})
			actionsLog.push({
				turn,
				action: 'playCard',
				card: card.name,
				target,
				energy_after: state.player.currentEnergy,
			})
			played = true
			break
		}
	}

	state = game.actions.endTurn(state)

	turnsLog.push({
		turn,
		player_hp: state.player.currentHealth,
		energy: state.player.currentEnergy,
		hand_size: state.hand.length,
		room_type: room.type,
	})

	if (isCurrRoomCompleted(state)) {
		const move = nextMoveFromPath(state)
		if (move) {
			state = game.actions.move(state, {move})
			roomsCleared += 1
		}
	}
}

const endedAt = new Date().toISOString()

const output = {
	run_id: runId,
	started_at: startedAt,
	ended_at: endedAt,
	metrics: {
		turns: turnsLog.length,
		rooms_cleared: roomsCleared,
		won: Boolean(state.won),
		player_hp: state.player.currentHealth,
	},
	actions: actionsLog,
	turns: turnsLog,
}

fs.mkdirSync(outDir, {recursive: true})
const outPath = path.join(outDir, `${runId}.json`)
fs.writeFileSync(outPath, JSON.stringify(output, null, 2))

console.log(`Autoplay run saved: ${outPath}`)
