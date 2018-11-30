#!/bin/bash
until python application.py; do
    echo "Collision detector crashed with exit code $?.  Respawning.." >&2
done
