#!/bin/bash
# CapCut AI GOD - Termux Setup
# Run: bash setup_termux.sh

echo "⚡ CapCut AI GOD - Termux Setup by R4X"
echo "========================================"

# Update packages
pkg update -y && pkg upgrade -y

# Install Python
pkg install python -y
pkg install python-pip -y

# Install required packages
pip install requests pillow

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 USAGE:"
echo "  1. Open CapCut AI GOD app on phone"
echo "  2. Tap 'START AI BOT SERVER'"
echo "  3. Set your OpenRouter API key in Settings"
echo "  4. Run: python capcut_bot.py"
echo ""
echo "🔑 Get free API key at: openrouter.ai"
echo "📱 Recommended model: anthropic/claude-opus-4 (best vision)"
echo ""
echo "Or set API key as env variable:"
echo "  export OPENROUTER_API_KEY=sk-or-v1-your-key"
echo "  python capcut_bot.py"
