/**
 * Complete AutoPlayer Test - Waits for full completion
 * 
 * This script runs AutoPlayer and waits for it to actually complete,
 * taking screenshots at key milestones.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.join(__dirname, '../screenshots/autoplayer_complete');
const GAME_FILE = path.join(__dirname, '../index_v2.html');

async function waitForAutoPlayerComplete(page, maxWait = 120000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < maxWait) {
        const status = await page.evaluate(() => {
            if (window.autoPlayer) {
                const progress = window.autoPlayer.getProgress();
                const isRunning = window.autoPlayer.isRunning;
                const logContent = document.getElementById('auto-player-log')?.textContent || '';
                return {
                    ...progress,
                    isRunning,
                    logContent: logContent.substring(logContent.length - 200) // Last 200 chars
                };
            }
            return null;
        }).catch(() => null);
        
        if (status) {
            console.log(`Progress: ${status.progress} | Scene: ${status.currentScene} | Running: ${status.isRunning}`);
            
            // Check if completed
            if (!status.isRunning || status.logContent.includes('COMPLETE') || status.logContent.includes('complete')) {
                return true;
            }
            
            // Check if stopped (not running and not paused)
            if (!status.isRunning && status.currentStep >= status.totalSteps) {
                return true;
            }
        }
        
        await page.waitForTimeout(2000); // Check every 2 seconds
    }
    
    return false;
}

async function testAutoPlayerComplete() {
    console.log('🎬 Starting complete AutoPlayer test...');
    
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
        console.log(`📂 Loading: ${gamePath}`);
        await page.goto(gamePath, { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(5000); // Wait for game to fully load
        
        // Screenshot 1: Initial load
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_initial_load.png'), fullPage: true });
        console.log('✅ Screenshot 1: Initial load');
        
        // Wait for AutoPlayer button
        await page.waitForSelector('#auto-player-btn', { timeout: 10000 });
        await page.waitForTimeout(1000);
        
        // Screenshot 2: Before start
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_before_start.png'), fullPage: true });
        console.log('✅ Screenshot 2: Before AutoPlayer start');
        
        // Start AutoPlayer
        console.log('▶️ Starting AutoPlayer...');
        await page.click('#auto-player-btn');
        await page.waitForTimeout(1000);
        
        // Screenshot 3: Started
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03_autoplayer_started.png'), fullPage: true });
        console.log('✅ Screenshot 3: AutoPlayer started');
        
        // Wait for Lab Scene and take screenshot
        await page.waitForTimeout(3000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_lab_scene.png'), fullPage: true });
        console.log('✅ Screenshot 4: Lab Scene');
        
        // Wait for Lobby transition
        await page.waitForTimeout(10000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05_lobby_scene.png'), fullPage: true });
        console.log('✅ Screenshot 5: Lobby Scene');
        
        // Wait for Underground transition
        await page.waitForTimeout(15000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06_underground_scene.png'), fullPage: true });
        console.log('✅ Screenshot 6: Underground Scene');
        
        // Wait for Void Scene
        await page.waitForTimeout(20000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07_void_scene_start.png'), fullPage: true });
        console.log('✅ Screenshot 7: Void Scene (Boss Fight)');
        
        // Wait for boss fight progress - Phase 1
        await page.waitForTimeout(15000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08_boss_phase1.png'), fullPage: true });
        console.log('✅ Screenshot 8: Boss Phase 1');
        
        // Wait for Phase 2
        await page.waitForTimeout(20000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '09_boss_phase2.png'), fullPage: true });
        console.log('✅ Screenshot 9: Boss Phase 2');
        
        // Wait for Phase 3
        await page.waitForTimeout(20000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '10_boss_phase3.png'), fullPage: true });
        console.log('✅ Screenshot 10: Boss Phase 3');
        
        // Wait for ending choice
        await page.waitForTimeout(15000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '11_ending_choice.png'), fullPage: true });
        console.log('✅ Screenshot 11: Ending Choice');
        
        // Wait for completion (with polling)
        console.log('⏳ Waiting for AutoPlayer to complete...');
        const completed = await waitForAutoPlayerComplete(page, 60000);
        
        // Final screenshot
        await page.waitForTimeout(3000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '12_completion.png'), fullPage: true });
        console.log('✅ Screenshot 12: Final state');
        
        // Get final status
        const finalStatus = await page.evaluate(() => {
            if (window.autoPlayer) {
                return window.autoPlayer.getProgress();
            }
            return null;
        }).catch(() => null);
        
        if (finalStatus) {
            console.log('\n📊 Final Status:');
            console.log(`   Progress: ${finalStatus.progress}`);
            console.log(`   Step: ${finalStatus.currentStep}/${finalStatus.totalSteps}`);
            console.log(`   Scene: ${finalStatus.currentScene}`);
            console.log(`   Running: ${finalStatus.isRunning}`);
            console.log(`   Paused: ${finalStatus.isPaused}`);
        }
        
        const logContent = await page.textContent('#auto-player-log').catch(() => '');
        if (logContent.includes('COMPLETE') || logContent.includes('complete')) {
            console.log('\n✅ AutoPlayer completed successfully!');
        } else {
            console.log('\n⚠️ AutoPlayer may not have fully completed');
            console.log(`Last log entries: ${logContent.substring(Math.max(0, logContent.length - 300))}`);
        }
        
        console.log(`\n📸 Screenshots: ${SCREENSHOT_DIR}`);
        
    } catch (error) {
        console.error('❌ Error:', error);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'error.png'), fullPage: true });
        throw error;
    } finally {
        await browser.close();
    }
}

if (require.main === module) {
    testAutoPlayerComplete().catch(console.error);
}

module.exports = { testAutoPlayerComplete };
