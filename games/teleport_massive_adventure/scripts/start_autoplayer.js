/**
 * Start AutoPlayer Script
 * 
 * This script can be used to programmatically start the AutoPlayer
 * from command line, automation tools, or AI agents.
 */

const { chromium } = require('playwright');

async function startAutoPlayer() {
    console.log('🎬 Starting AutoPlayer via automation...');
    
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1200, height: 800 }
    });
    const page = await context.newPage();
    
    try {
        // Load game with auto parameter
        const gameUrl = 'http://localhost:8000/index_v2.html?auto=true';
        console.log(`📂 Loading: ${gameUrl}`);
        await page.goto(gameUrl, { waitUntil: 'networkidle', timeout: 30000 });
        
        // Wait for game to load
        await page.waitForTimeout(3000);
        
        // Check if AutoPlayer started automatically
        const autoStarted = await page.evaluate(() => {
            return window.autoPlayer?.isRunning || false;
        });
        
        if (autoStarted) {
            console.log('✅ AutoPlayer started automatically from URL parameter!');
        } else {
            // Fallback: Click the button programmatically
            console.log('🖱️ Clicking AutoPlayer button...');
            await page.click('#auto-player-btn');
            await page.waitForTimeout(500);
            
            const started = await page.evaluate(() => {
                return window.autoPlayer?.isRunning || false;
            });
            
            if (started) {
                console.log('✅ AutoPlayer started via button click!');
            } else {
                console.log('⚠️ AutoPlayer may not have started. Check browser console.');
            }
        }
        
        // Get status
        const status = await page.evaluate(() => {
            if (window.autoPlayer) {
                return window.autoPlayer.getProgress();
            }
            return null;
        });
        
        if (status) {
            console.log(`📊 Status: ${status.progress} | Scene: ${status.currentScene}`);
        }
        
        console.log('\n✅ Game is running! AutoPlayer should be active.');
        console.log('💡 Keep this terminal open - browser will close when script exits.');
        console.log('💡 Press Ctrl+C to stop.');
        
        // Keep browser open
        await new Promise(() => {}); // Wait indefinitely
        
    } catch (error) {
        console.error('❌ Error:', error);
        await browser.close();
        process.exit(1);
    }
}

if (require.main === module) {
    startAutoPlayer().catch(console.error);
}

module.exports = { startAutoPlayer };
