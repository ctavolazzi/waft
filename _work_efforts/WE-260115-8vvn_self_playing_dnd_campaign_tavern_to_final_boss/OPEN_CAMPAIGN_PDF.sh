#!/bin/bash
# Quick script to open the campaign PDF

PDF_PATH="/Volumes/Easystore/waft/waft/_work_efforts/WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss/output/Self_Playing_DnD_Campaign_Complete.pdf"

if [ -f "$PDF_PATH" ]; then
    echo "🎲 Opening your DnD Campaign PDF..."
    open "$PDF_PATH"
    echo "✅ PDF opened!"
else
    echo "⚠️  PDF not found at: $PDF_PATH"
    echo "📋 Looking for PDF..."
    find /Volumes/Easystore/waft -name "Self_Playing_DnD_Campaign_Complete.pdf" -type f 2>/dev/null | head -1
fi
