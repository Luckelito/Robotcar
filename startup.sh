#!/bin/sh

if [-z$DESKTOP_SESSION];
then
echo "Not in the desktop"
else
python3 /home/pi/Documents/Robotcar/Main.py
fi