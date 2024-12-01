#!/bin/bash
while true; do
    git add .
    git commit -m "Automatic commit"
    git push origin main
    sleep 1
done