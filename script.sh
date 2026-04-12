#!/bin/bash

sudo apt update
sudo apt install scrot python3-tk python3-dev xdotool -y

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 