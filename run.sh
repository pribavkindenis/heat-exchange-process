#!/usr/bin/env bash
if [[ -d "./venv" ]]
then
source ./venv/bin/activate
python3.6 main.py
deactivate
else
echo "You need to run install.sh first."
fi