![banner](./banner.png)

# Piglet

Piglet is a library of search algorithms and the domains they run on. It ships a small command-line
tool for running scenarios and generating search traces, and a Python API you can reuse in your own
code.

> **This is the labs branch.** Several library functions are left as stubs for you to implement
> during the lab exercises. Until you fill them in, grid searches return no successors and the grid
> heuristics raise `NotImplementedError`. The stubs are:
>
> - `lib_piglet/heuristics/gridmap_h.py` — `manhattan_heuristic`, `straight_heuristic`,
>   `octile_heuristic`, `differential_heuristic`
> - `lib_piglet/expanders/grid_expander.py` — `grid_expander.expand` / `get_actions` / `__move`, and
>   `grid_joint_expander.expand` / `generate_states_recursively`
> - `lib_piglet/search/iterative_deepening.py` — cost-threshold (IDA\*) support
>
> Each stub is marked with an `Implement your codes here` comment.

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
