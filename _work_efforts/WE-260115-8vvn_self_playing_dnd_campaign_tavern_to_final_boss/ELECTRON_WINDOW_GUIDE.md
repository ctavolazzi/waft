# Electron Window Guide - Watch the Game Play!

**How to see the DnD game playing itself in an Electron window**

---

## 🎯 What You'll See

An Electron window that shows:
- ✅ Party members with HP bars
- ✅ Current scene/encounter
- ✅ Real-time campaign log
- ✅ Encounters as they happen
- ✅ Leveling up animations
- ✅ Final boss battle
- ✅ Victory screen!

---

## 🚀 How to Run

### Option 1: Use the Electron Version

```bash
./run_campaign_electron.sh
```

This will:
1. Start the campaign
2. Open an Electron window (or browser if Electron not available)
3. Show the game playing in real-time
4. Update every 2 seconds
5. Generate PDF at the end

### Option 2: Run Directly

```bash
python3 SELF_PLAYING_CAMPAIGN_ELECTRON.py
```

---

## 🪟 What Opens

### Electron Window (Preferred)

If Electron is available, you'll see:
- Beautiful window with D&D theme
- Real-time updates
- Party stats
- Encounter log
- Campaign progress

### Browser Fallback

If Electron isn't available:
- Opens in your default browser
- Same beautiful interface
- Still auto-refreshes
- Still shows everything

---

## 📊 What's Displayed

### Party Section

- **Character Names** - Thorin, Lyra, Rogar, Aria
- **Class & Race** - Dwarf Fighter, Elf Wizard, etc.
- **HP Bars** - Visual health indicators
- **Level** - Current level
- **XP** - Experience points

### Current Scene

- **Location** - Where the party is
- **Action** - What's happening now
- **Updates** - Changes in real-time

### Encounters

- **Encounter Name** - Goblin Ambush, etc.
- **Description** - What happened
- **Rounds** - How long the battle lasted
- **XP Gained** - Experience earned

### Campaign Log

- **Real-time Events** - Everything as it happens
- **Last 10 Entries** - Most recent activity
- **Auto-updates** - Refreshes every 2 seconds

---

## ⚙️ Technical Details

### How It Works

1. **Python Script** - Runs the campaign
2. **HTML Generator** - Creates beautiful HTML
3. **Auto-Refresh** - HTML refreshes every 2 seconds
4. **Electron/Browser** - Displays the HTML
5. **Real-time Updates** - See everything as it happens

### File Location

The HTML file is created at:
```
output/campaign_display.html
```

This file is updated in real-time as the campaign progresses.

---

## 🎮 Experience

### What You'll See

1. **Window Opens** - Electron or browser window appears
2. **Party Spawns** - 4 heroes appear with stats
3. **Tavern Scene** - Opening scene displays
4. **Encounters** - Each battle shown in real-time
5. **Leveling** - See characters level up
6. **Final Boss** - Epic battle displayed
7. **Victory** - Celebration screen!

### Timing

- **2-second updates** - Window refreshes every 2 seconds
- **Real-time feel** - See everything as it happens
- **Smooth experience** - Beautiful animations

---

## 🔧 Troubleshooting

### "Electron window not opening"

**Solution**: The script will fallback to browser automatically. You'll still see everything!

### "Window not updating"

**Check**: Make sure the HTML file exists:
```bash
ls -la output/campaign_display.html
```

### "Want to use Electron specifically"

**Option 1**: Install Electron globally:
```bash
npm install -g electron
```

**Option 2**: Use the Dockerized Electron app:
```bash
cd recap_review_app/frontend
docker-compose up -d electron-app
```

---

## 💡 Tips

1. **Keep Window Open** - Don't close it during the campaign
2. **Watch the Log** - See events as they happen
3. **Check HP Bars** - Watch party health change
4. **See Leveling** - Watch characters level up
5. **Final Boss** - Epic battle displayed!

---

## 🎉 The Experience

You wanted to:
> "See the game playing itself"

**Now you can!**

- ✅ Electron window opens
- ✅ Party appears
- ✅ Story unfolds in real-time
- ✅ Encounters happen
- ✅ Final boss battle
- ✅ Victory celebration

**Watch the DnD game play itself!**

---

**Status**: ✅ **Electron Window Version Ready!**

🎲 **Run `./run_campaign_electron.sh` to see it in action!** 🎲
