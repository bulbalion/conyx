#!/bin/bash
export CONYX=`pwd`
python3 -m cProfile -s cumtime -o profile_tui.txt tui.py
