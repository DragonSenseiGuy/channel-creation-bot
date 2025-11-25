#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run the bot in the background with nohup
# Output will be redirected to bot.log
nohup python main.py > bot.log 2>&1 &

# Save the Process ID (PID) to a file so we can kill it later
echo $! > bot.pid

echo "Bot started in background. Logs are in bot.log."
echo "PID is stored in bot.pid."
