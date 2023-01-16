#!/bin/bash
echo "Running..."
pkill -F pid.pid
source ./venv/bin/activate
python tauben_bot.py &
echo $! > pid.pid