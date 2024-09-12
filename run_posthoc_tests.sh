#!/bin/bash

# Graph BFS
python piglet.py -p ./example/arena2.map.scen -f graph -s breadth --log trace out/bfs.trace.yaml -t 0.1 -x 2 -n 1
# Graph DFS
python piglet.py -p ./example/arena2.map.scen -f graph -s depth --log trace out/dfs.trace.yaml -t 0.05 -x 2 -n 1
# Tree BFS
python piglet.py -p ./example/arena2.map.scen -f tree -s breadth --log trace out/tree.trace.yaml -t 0.1 -x 2 -n 1
# IDDFS
python piglet.py -p ./example/arena2.map.scen -f iterative -s depth --log trace out/iddfs.trace.yaml -t 0.1 -x 2 -n 1
# Uniform
python piglet.py -p ./example/arena2.map.scen -f graph -s uniform --log trace out/uniform.trace.yaml -t 0.1 -x 2 -n 1
# A*
python piglet.py -p ./example/arena2.map.scen -f graph -s a-star --log trace out/a-star.trace.yaml -x 100 -n 1
