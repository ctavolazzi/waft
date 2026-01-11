# Global Commands Setup

**Purpose:** Make WAFT scripts available globally from anywhere in your system

---

## Quick Setup

### Option 1: Add to PATH (Recommended)

Add this line to your `~/.zshrc` (or `~/.bashrc`):

```bash
export PATH="$PATH:/Users/ctavolazzi/Code/active/waft/scripts"
```

Then reload:
```bash
source ~/.zshrc
```

### Option 2: Create Symlink

```bash
# Create symlink in /usr/local/bin (requires sudo)
sudo ln -s /Users/ctavolazzi/Code/active/waft/scripts/waft-one-pager-chat /usr/local/bin/waft-one-pager-chat

# Or in your local bin (no sudo needed)
mkdir -p ~/bin
ln -s /Users/ctavolazzi/Code/active/waft/scripts/waft-one-pager-chat ~/bin/waft-one-pager-chat
export PATH="$PATH:$HOME/bin"
```

---

## Available Global Commands

### `waft-one-pager-chat`

Creates a one-pager PDF from the current chat session.

**Usage:**
```bash
waft-one-pager-chat
```

**Output:**
- `_work_efforts/one_pagers/chat_session_[date]_[time].pdf`
- Automatically opens the PDF
- Perfect 2-page document (front/back)

**Works from:** Anywhere in your system

---

## Verification

After setup, verify it works:

```bash
# Should show the script path
which waft-one-pager-chat

# Should run successfully
waft-one-pager-chat
```

---

## Troubleshooting

### "Command not found"

1. Check PATH includes scripts directory:
   ```bash
   echo $PATH | grep waft
   ```

2. Verify script is executable:
   ```bash
   ls -l /Users/ctavolazzi/Code/active/waft/scripts/waft-one-pager-chat
   ```

3. Reload shell:
   ```bash
   source ~/.zshrc
   ```

### "Module not found"

The script automatically finds the project root. If you get import errors:
- Make sure you're in the WAFT project directory, OR
- The script should auto-detect the project root

---

**Status:** Ready to use globally!
