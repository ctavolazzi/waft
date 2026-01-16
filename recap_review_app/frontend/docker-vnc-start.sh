#!/bin/bash
# VNC startup script for Electron app

set -e

# Set VNC password
echo "$VNC_PASSWORD" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

# Start VNC server
vncserver :1 -geometry 1024x768 -depth 24

# Start window manager
export DISPLAY=:1
fluxbox &

# Wait for display to be ready
sleep 2

# Start Electron app
npm start
