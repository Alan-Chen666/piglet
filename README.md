![banner](./banner.png)

# Piglet

Piglet is a library of search algorithms and the domains they run on. It ships a small command-line
tool for running scenarios and generating search traces, and a Python API you can reuse in your own
code.

> **New to terminals, Git or Python environments?** Follow [GETTING_STARTED.md](GETTING_STARTED.md)
> first — it installs the tooling and ends with a search running on your screen. The rest of this
> README assumes you are comfortable with the tooling.

## Requirements

- [uv](https://docs.astral.sh/uv/) — the only thing you need to install yourself.

uv provisions the correct Python interpreter (3.14.6, pinned in `.python-version`) and every
dependency for you. You do not need to install Python separately.

## Setup

Clone the repo, then run a scenario straight away:

```bash
uv run piglet -p ./example/example_n_puzzle_scenario.scen -f graph -s uniform
```

There is no separate install step. The first `uv run` creates a virtual environment in `.venv` and
installs the dependencies; this takes a moment. Later runs skip it and start immediately. Prefixing a
command with `uv run` runs it inside that environment, so there is no `activate` step to remember.

## Piglet command line

```bash
uv run piglet --help
```

Run a scenario, choosing a domain (`-f`) and a search (`-s`):

```bash
uv run piglet -p ./example/arena2.min.scen -f graph -s a-star
uv run piglet -p ./example/arena2.min.scen -f graph -s uniform    # compare the nodes expanded
```

### Generating search traces

Use search traces to analyse and debug algorithms in [Posthoc](https://posthoc.pathfinding.ai). Add
the `--log trace` argument to make Piglet output search traces.

```bash
uv run piglet -p ./example/arena2.min.scen -f graph -s a-star --log trace
```

## Scenario and map files

The `-p` argument takes a scenario file: a header naming the domain, then one problem per line. Grid
problems name a map file that holds the terrain. Both formats come from the
[Moving AI benchmark suite](https://movingai.com/benchmarks/formats.html), with the differences noted
below.

Piglet skips blank lines and any line whose first whitespace-separated token is `#` or `c`, so leave a
space after the `#`. Columns can be separated by tabs or spaces. Drop `-p` and piglet reads the
scenario from standard input instead.

### The header line

The first line that is not a comment says which domain the problems belong to:

```
domain grid4
```

The domain types are `grid4`, `n-puzzle`, `graph` and `pddl`. Scenarios downloaded from Moving AI
open with `version 1` instead; replace that line with `domain grid4` or piglet rejects the file.

### Grid problems

Every line carries the nine columns of a Moving AI scenario:

| # | Column | Read by piglet |
|---|--------|----------------|
| 1 | bucket | no |
| 2 | map file | yes |
| 3 | map width | no |
| 4 | map height | no |
| 5 | start x (column) | yes |
| 6 | start y (row) | yes |
| 7 | goal x (column) | yes |
| 8 | goal y (row) | yes |
| 9 | optimal length | no |

Four of the columns go unread, but a line still has to supply all nine.

The map path is resolved against your working directory, not against the scenario file. The bundled
scenarios use paths like `./example/gridmap/arena2.map`, so run them from the repository root.

Coordinates follow the Moving AI convention, where x counts columns from the left and y counts rows
from the top. A piglet grid state is a `(row, column)` tuple, so a problem that starts at x 4, y 0
prints as `(0, 4)`.

```
domain grid4
# bucket  map  width  height  start_x  start_y  goal_x  goal_y  optimal_length
0   ./example/gridmap/empty-16-16.map  16  16  1  2  9  2  -1
```

`example/example_grid_scenario.scen` is an annotated example, and `example/arena2.min.scen` is a
single problem on a larger map.

### Map files

A map is an octile file: a four line header followed by one line per row.

```
type octile
height 8
width 8
map
........
........
```

The body holds `height` rows of `width` characters. Moving AI defines several terrain characters, of
which `.` and `G` are passable ground, `S` is swamp, `T` is trees, and `@` or `O` mark cells outside
the map. Piglet is stricter: only `.` is traversable, and every other character blocks. Convert the
`G` and `S` tiles before running a map that uses them.

The header says `octile`, but the `grid4` domain moves up, down, left and right only, and each move
costs 1.

### The other domains

Scenarios for the remaining domains use the same file extension and the same one problem per line
layout.

- `n-puzzle`: the puzzle width, then the start tiles in row-major order, comma separated, writing the
  blank as `x` or `0`. The goal is always the blank followed by the tiles in order, `x,1,2,3,...`.
- `graph`: the graph file, the start node id, the goal node id, and an optimal length that piglet
  ignores but still expects. Graph files use the DIMACS 9th Challenge format.
- `pddl`: a domain file and a problem file.

For each of these see `example/example_n_puzzle_scenario.scen`, `example/example_sample_graph.scen`
and `example/example_pddl.scen`.

## Piglet library

To run a search you need three things: a domain, an expander, and a search.

```python
from lib_piglet.domains import gridmap
from lib_piglet.expanders.grid_expander import grid_expander
from lib_piglet.search.graph_search import graph_search
from lib_piglet.search.search_node import compare_node_f
from lib_piglet.utils.data_structure import bin_heap
from lib_piglet.heuristics import gridmap_h

# a gridmap domain, and an expander that generates its successors
gm = gridmap.gridmap("./example/gridmap/empty-16-16.map")
expander = grid_expander(gm)

# a search, given an open list (a binary heap ordered on f) and the expander
search = graph_search(
    bin_heap(compare_node_f),
    expander,
    heuristic_function=gridmap_h.piglet_heuristic,
)

# for a gridmap, a state is an (x, y) tuple
solution = search.get_path((1, 2), (10, 2))
print(solution)
```

Every heuristic takes `(domain, current_state, goal_state)`, so any of them can be handed straight to a search. `piglet_heuristic` is the default each domain uses from the command line; swap in `gridmap_h.octile_heuristic`, `gridmap_h.straight_heuristic` or your own to compare. Use `compare_node_g` instead of `compare_node_f` for an uninformed search.
