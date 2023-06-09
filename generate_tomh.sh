#!/bin/sh

# Generate data
python3.10 create_world.py
# python3.10 generate_tasks.py -w world_large.txt -n 20 -ptn=0.1
# python3.10 generate_tasks.py -w world_large.txt -n 20 -ptn=0.1 --tell True
python3.10 generate_prompts.py