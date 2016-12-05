#!/bin/bash
while ! (bash ./wait-for-it.sh db:5432); do sleep 4; done
echo "Starting the program";
python botme.py