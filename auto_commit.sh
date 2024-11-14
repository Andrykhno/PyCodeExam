#!/bin/bash
while true; do
    git add .
    git commit -m "Автоматический коммит"
    git push origin main
    sleep 600
done