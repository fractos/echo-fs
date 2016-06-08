#!/bin/bash

cd /opt/echo-fs

echo "Activating python virtual environment"
source venv/bin/activate

echo "Starting echo-scavenger with Redis address of $1"

python echo_scavenger.py $1
