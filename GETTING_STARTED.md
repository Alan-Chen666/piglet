# 🐷 Getting Started with Piglet
========

This guide takes you from a fresh computer to a search running on your screen. It assumes no prior
experience with terminals, Git or Python environments; if you have used them before, skip ahead.

You install just two things — **Git**, to download the code, and **uv**, to manage Python. uv
downloads the right Python interpreter and every dependency for you the first time you run Piglet;
you never install Python yourself.

Piglet is tested with Python 3.14 on modern versions of Windows, macOS and Linux, and inside WSL
(Windows Subsystem for Linux).

- [Step 1: Install Git](#step-1-install-git)
- [Step 2: Install uv](#step-2-install-uv)
- [Step 3: Download Piglet](#step-3-download-piglet)
- [Step 4: Run a search](#step-4-run-a-search)
- [Step 5: Use the library](#step-5-use-the-library)
- [Troubleshooting](#troubleshooting)

---

Step 1: Install Git
---

**Git** downloads the code and tracks changes to your own work. First check whether you have it:

```console
$ git --version
```

If that prints a version number, skip to [Step 2](#step-2-install-uv). Otherwise install it:

| Platform | Command |
| --- | --- |
| Windows | `winget install --id Git.Git -e` |
| WSL / Ubuntu / Debian | `sudo apt update && sudo apt install git` |
| macOS | `xcode-select --install` |
| Fedora | `sudo dnf install git` |
| Arch | `sudo pacman -S git` |

**Close your terminal and open a new one**, then confirm it worked with `git --version`.

> **Why a new terminal?** A terminal reads the list of available commands once, when it starts. A
> program installed afterwards is invisible to it until you open a fresh one.

---

Step 2: Install uv
---

**uv** manages Python for you, so do not install Python yourself. It reads the `.python-version`
file, downloads the interpreter it names (currently 3.14.6), and keeps it isolated from the rest of
your machine.

**Windows** (PowerShell):

```console
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS, Linux and WSL**:

```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Close your terminal and open a new one**, then check with `uv --version`. Any version number means
you are fine; if it says *command not found*, see [Troubleshooting](#uv-command-not-found).

---

Step 3: Download Piglet
---

Choose where to keep the code and move there (`cd` means "change directory"), then clone the repo:

```console
$ cd Documents
$ git clone <the-piglet-repository-url>
$ cd <the-folder-it-created>
```

You are now *inside* the project folder, which is where every remaining command must be run. Check
you are in the right place; you should see `pyproject.toml`:

```console
$ ls          # Windows PowerShell: dir
```

> **WSL users**: keep your code in the Linux home directory (`~`), not in `/mnt/c/...`. Working
> across the Windows/Linux boundary is dramatically slower.

---

Step 4: Run a search
---

There is no install step. Just run a scenario:

```console
$ uv run piglet -p ./example/example_n_puzzle_scenario.scen -f graph -s uniform
```

The first time, this sits there for a moment while `uv run` sets the project up: it reads
`.python-version` and `pyproject.toml`, downloads the right Python, and installs the dependencies at
the versions pinned in `uv.lock`, all into `.venv`. Later runs start immediately.

> **Always use `uv run`.** It runs your command inside the project's environment. `uv run piglet ...`
> works; plain `piglet ...` uses whatever Python happens to be on your machine.

Try a few more, and compare how the searches differ:

```console
$ uv run piglet -p ./example/arena2.min.scen -f graph -s a-star
$ uv run piglet -p ./example/arena2.min.scen -f graph -s uniform    # compare the nodes expanded
$ uv run piglet --help
```

Add `--log trace` to record a search trace, then load it into
[Posthoc](https://posthoc.pathfinding.ai) and step through the search node by node:

```console
$ uv run piglet -p ./example/arena2.min.scen -f graph -s a-star --log trace
```

---

Step 5: Use the library
---

Piglet is also a Python library. A search needs three things: a **domain**, an **expander** that
generates a state's successors, and a **search** that puts them together.

```python
from lib_piglet.domains import gridmap
from lib_piglet.expanders.grid_expander import grid_expander
from lib_piglet.search.graph_search import graph_search
from lib_piglet.search.search_node import compare_node_f
from lib_piglet.utils.data_structure import bin_heap
from lib_piglet.heuristics import gridmap_h

gm = gridmap.gridmap("./example/gridmap/empty-16-16.map")
expander = grid_expander(gm)

search = graph_search(
    bin_heap(compare_node_f),                       # open list, ordered on f
    expander,
    heuristic_function=gridmap_h.piglet_heuristic,
)

solution = search.get_path((1, 2), (10, 2))
print(solution)
```

See [README.md](README.md) for more on the library and its command line.

---

Troubleshooting
---

### `uv`: command not found

You almost certainly need to open a new terminal — see the note at the end of
[Step 1](#step-1-install-git). If a fresh terminal still cannot find it, the installer put `uv`
somewhere your terminal does not look. Fix it for the current terminal with:

**macOS / Linux / WSL:**

```console
$ export PATH="$HOME/.local/bin:$PATH"
```

**Windows:**

```console
> $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
```

That lasts until you close the terminal. To make it permanent, restart your machine and try again in
a new terminal.

### Something else

Include your operating system, the command you ran, and the complete error message when you ask for
help; a screenshot of a single line is rarely enough to diagnose anything.
