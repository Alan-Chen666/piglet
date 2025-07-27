python piglet.py -p ./example/arena2.map.scen -f graph -s a-star --log trace out/news/my-trace.trace.yaml -x 30 -n 1
python piglet.py -p ./example/arena2.map.scen -f graph -s breadth --log trace out/news/bfs.trace.yaml -t 0.05 -x 2 -n 1
python piglet.py -p ./example/arena2.map.scen -f graph -s depth --log trace out/news/dfs.trace.yaml -t 0.05 -x 2 -n 1
python piglet.py -p ./example/arena2.map.scen -f graph -s a-star --log trace out/news/astar.trace.yaml -x 100 -n 1
python piglet.py -p ./example/example_8_puzzle.scen -f tree -s a-star --log trace out/news/nine-tiles.trace.yaml -x 1 -n 1
python piglet.py -p ./example/arena2.map.scen -f graph -s a-star --heuristic-weight 0.5 --log trace out/news/astar-half-h.trace.yaml -x 50 -n 1
python piglet.py -p ./example/arena2.map.scen -f graph -s a-star --heuristic-weight 0 --log trace out/news/astar-zero-h.trace.yaml -x 50 -n 1
