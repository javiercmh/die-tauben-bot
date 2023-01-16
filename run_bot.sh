#!/bin/bash
echo "Running..."
git pull
pkill -INT -F pid.pid
source ./venv/bin/activate
python tauben_bot.py &
echo $! > pid.pid