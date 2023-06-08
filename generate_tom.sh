#!/bin/sh
python3.10 create_world.py
python3.10 generate_tasks.py -w world_large.txt -n 1 -ptn=0 --prompt MC
python3.10 generate_tasks.py -w world_large.txt -n 1 -ptn=0 --prompt CoT
python3.10 generate_tasks.py -w world_large.txt -n 1 -ptn=0 --tell True --prompt MC
python3.10 generate_tasks.py -w world_large.txt -n 1 -ptn=0 --tell True --prompt CoT