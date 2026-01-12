#!/bin/bash
# Open iTerm in a small window and run hello world script

osascript <<EOF
tell application "iTerm"
    activate
    set newWindow to (create window with default profile)
    tell current session of newWindow
        write text "cd /Users/ctavolazzi/Code/active/waft && python3 hello_world.py"
    end tell
    set bounds of newWindow to {100, 100, 600, 400}
end tell
EOF
