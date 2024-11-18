#!/bin/bash
while true; do
    git add .
    git commit -m "Автоматический коммит"
    git push origin main
    sleep 60
done