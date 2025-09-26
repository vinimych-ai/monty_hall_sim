# Monty Hall Simulator (Python)

A minimal, fast Monty Hall problem simulator.

* Fixes the player's initial door to `0` (by symmetry).
* Scores **both** strategies (stay vs. switch) from the same trials.
* Optional `--debug` checks enforce Monty’s host rules.
* Clean **Ctrl+C** interrupt prints partial results.
* Prints win rates with simple 95% confidence intervals.

---

## Requirements

* Python 3.8+ (CPython recommended)

No third-party packages required.

---

## Usage

```bash
python monty_hall_sim.py <sim_target> [--seed SEED] [--debug]
```

### Arguments

* `sim_target` *(int, required)* — number of simulations to run (>= 1).
* `--seed SEED` *(int, optional)* — RNG seed for reproducibility.
* `--debug` *(flag, optional)* — enable per-round invariant checks (slower).

### Examples

**Windows PowerShell**

```powershell
python .\monty_hall_sim.py 200000
python .\monty_hall_sim.py 200000 --seed 42
python .\monty_hall_sim.py 1000000 --debug
```

**bash / zsh**

```bash
python monty_hall_sim.py 200000
python monty_hall_sim.py 200000 --seed 42
python monty_hall_sim.py 1000000 --debug
```

### Interrupting a long run

Press **Ctrl+C** to stop early; the program will report **partial results** computed so far.

---

## What it prints

* Wins/losses for **Stay** and **Switch**.
* Win rates as percentages.
* Simple 95% confidence intervals (normal approximation).

Example:

```
Trials: 200,000 | Seed: 42
Stay:   wins=66,758  losses=133,242   win-rate=33.379%   95% CI [33.123% , 33.635%]
Switch: wins=133,242  losses=66,758   win-rate=66.621%   95% CI [66.365% , 66.877%]
```

---

## How it works (brief)

* Player’s initial choice is fixed to door `0` (labels are symmetric).
* Prize is placed uniformly at random among `{0,1,2}`.
* Host opens a goat door: never the player’s door, never the prize; ties broken uniformly.
* From each trial, we can infer outcomes for **both** strategies:

  * If `prize == 0`: staying wins, switching loses.
  * Otherwise: switching wins, staying loses.

`--debug` adds invariant checks to catch any violation of Monty’s rules.

---

## Performance notes

* CPU-bound on a single core; memory usage is O(1).
* Avoid printing inside the loop.
* Typical CPython throughput: a few million trials/second per core.
  For very large runs, consider multiprocessing, PyPy, or JIT/compiled options.

---

## License

MIT — see [LICENSE](./LICENSE).
