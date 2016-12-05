#!/bin/bash
while ! (bash ./wait-for-it.sh db:5432); do sleep 1; done
echo "Starting the server";
python botme.py