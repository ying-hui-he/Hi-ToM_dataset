#!/bin/sh

# Generate data
python create_world.py
python generate_tasks.py -w world_large.txt -n 20 -ptn=0.1
python generate_tasks.py -w world_large.txt -n 20 -ptn=0.1 --tell True
python generate_prompts.py