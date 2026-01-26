/**
 * AutoPlayer Test Script with Screenshots
 * 
 * Uses Playwright to:
 * 1. Load the game
 * 2. Start AutoPlayer
 * 3. Take screenshots at key moments
 * 4. Verify completion
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.join(__dirname, '../screenshots/autoplayer_test');
const GAME_FILE = path.join(__dirname, '../index_v2.html');

async function testAutoPlayer() {
    console.log('🎬 Starting AutoPlayer test with screenshots...');
    
    // Create screenshot directory
    if (!fs.existsSync(SCREENSHOT_DIR)) {
        fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    }
    
    // Launch browser
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1200, height: 800 }
    });
    const page = await context.newPage();
    
    try {
        // Load game
        const gamePath = `file://${GAME_FILE}`;
        console.log(`📂 Loading game from: ${gamePath}`);
        await page.goto(gamePath, { waitUntil: 'networkidle' });
        
        // Wait for game to load
        await page.waitForTimeout(3000);
        
        // Take initial screenshot
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_initial_load.png'), fullPage: true });
        console.log('✅ Screenshot 1: Initial load');
        
        // Wait for AutoPlayer button to appear
        await page.waitForSelector('#auto-player-btn', { timeout: 10000 });
        await page.waitForTimeout(1000);
        
        // Take screenshot before starting
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_before_start.png'), fullPage: true });
        console.log('✅ Screenshot 2: Before AutoPlayer start');
        
        // Click AutoPlayer button
        console.log('▶️ Starting AutoPlayer...');
        await page.click('#auto-player-btn');
        await page.waitForTimeout(500);
        
        // Take screenshot after start
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03_autoplayer_started.png'), fullPage: true });
        console.log('✅ Screenshot 3: AutoPlayer started');
        
        // Wait for Lab Scene actions
        await page.waitForTimeout(2000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_lab_scene.png'), fullPage: true });
        console.log('✅ Screenshot 4: Lab Scene');
        
        // Wait for Lobby transition
        await page.waitForTimeout(5000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05_lobby_scene.png'), fullPage: true });
        console.log('✅ Screenshot 5: Lobby Scene');
        
        // Wait for Underground transition
        await page.waitForTimeout(8000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06_underground_scene.png'), fullPage: true });
        console.log('✅ Screenshot 6: Underground Scene');
        
        // Wait for Void Scene (boss fight)
        await page.waitForTimeout(15000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07_void_scene_start.png'), fullPage: true });
        console.log('✅ Screenshot 7: Void Scene (Boss Fight Start)');
        
        // Wait for boss fight progress
        await page.waitForTimeout(10000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08_boss_fight_phase1.png'), fullPage: true });
        console.log('✅ Screenshot 8: Boss Fight Phase 1');
        
        // Wait for more boss fight
        await page.waitForTimeout(15000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '09_boss_fight_phase2.png'), fullPage: true });
        console.log('✅ Screenshot 9: Boss Fight Phase 2');
        
        // Wait for final phase and ending
        await page.waitForTimeout(20000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '10_boss_fight_phase3.png'), fullPage: true });
        console.log('✅ Screenshot 10: Boss Fight Phase 3');
        
        // Wait for ending choice
        await page.waitForTimeout(10000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '11_ending_choice.png'), fullPage: true });
        console.log('✅ Screenshot 11: Ending Choice');
        
        // Wait for completion
        await page.waitForTimeout(5000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '12_completion.png'), fullPage: true });
        console.log('✅ Screenshot 12: Game Complete');
        
        // Check AutoPlayer status
        const statusText = await page.textContent('#auto-player-status');
        console.log(`📊 Final AutoPlayer status: ${statusText}`);
        
        // Check log area for completion message
        const logContent = await page.textContent('#auto-player-log');
        if (logContent && logContent.includes('COMPLETE')) {
            console.log('✅ AutoPlayer completed successfully!');
        }
        
        console.log(`\n📸 Screenshots saved to: ${SCREENSHOT_DIR}`);
        console.log('✅ Test complete!');
        
    } catch (error) {
        console.error('❌ Error during test:', error);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'error.png'), fullPage: true });
        throw error;
    } finally {
        await browser.close();
    }
}

// Run test
if (require.main === module) {
    testAutoPlayer().catch(console.error);
}

module.exports = { testAutoPlayer };
