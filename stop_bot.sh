#!/bin/bash

if [ -f bot.pid ]; then
    PID=$(cat bot.pid)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "Bot stopped (PID $PID)."
        rm bot.pid
    else
        echo "Bot process $PID not found. Cleaning up pid file."
        rm bot.pid
    fi
else
    echo "No bot.pid file found. Is the bot running?"
fi
