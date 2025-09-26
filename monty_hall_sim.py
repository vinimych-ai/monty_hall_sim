import argparse
import random as rnd
import math

PLAYER = 0  # by symmetry we can fix the player's choice

def positive_int(s: str) -> int:
    try:
        v = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError("The number of simulations must be an integer")
    if v < 1:
        raise argparse.ArgumentTypeError("The number of simulations must be >= 1")
    return v

def parse_cli():
    p = argparse.ArgumentParser(description="Monty Hall simulation")
    p.add_argument("sim_target", type=positive_int,
                   help="number of simulations to run (>=1)")
    p.add_argument("--seed", type=int, default=None,
                   help="optional RNG seed for reproducibility")
    p.add_argument("--debug", action="store_true",
                   help="enable per-round invariant checks")
    return p.parse_args()

def pct(x: float) -> str:
    return f"{100 * x:.3f}%"

def ci(p: float, se: float) -> str:
    lo, hi = max(0.0, p - 1.96 * se), min(1.0, p + 1.96 * se)
    return f"[{pct(lo)} , {pct(hi)}]"

def print_report(stay_win, stay_lose, switch_win, switch_lose, n, seed):
    """Print results for n completed trials (works for partial runs too)."""
    if n == 0:
        print("No simulations completed.")
        return
    # per-strategy sanity checks (each strategy should have n outcomes)
    assert stay_win + stay_lose == n, f"stay counter mismatch: {stay_win + stay_lose} vs {n}"
    assert switch_win + switch_lose == n, f"switch counter mismatch: {switch_win + switch_lose} vs {n}"
    assert stay_win == switch_lose and stay_lose == switch_win, "cross-consistency failed"

    p_stay = stay_win / n
    p_switch = switch_win / n
    se_stay = math.sqrt(p_stay * (1 - p_stay) / n)
    se_switch = math.sqrt(p_switch * (1 - p_switch) / n)

    seed_str = seed if seed is not None else "OS entropy"
    print(f"Trials: {n:,} | Seed: {seed_str}")
    print(f"Stay:   wins={stay_win:,}  losses={stay_lose:,}   "
          f"win-rate={pct(p_stay)}   95% CI {ci(p_stay, se_stay)}")
    print(f"Switch: wins={switch_win:,}  losses={switch_lose:,}   "
          f"win-rate={pct(p_switch)}   95% CI {ci(p_switch, se_switch)}")

def main():
    args = parse_cli()
    if args.seed is not None:
        rnd.seed(args.seed)

    sim_target = args.sim_target
    stay_win = stay_lose = switch_win = switch_lose = 0
    sim_counter = 0

    try:
        while sim_counter < sim_target:
            prize = rnd.randrange(3)

            # Host opens a valid goat door
            if prize == PLAYER:
                host = rnd.choice((1, 2))       # tie-break uniformly
            else:
                host = 3 - prize                # unique legal door when PLAYER=0

            # Optional invariant checks (dev only)
            if args.debug:
                if host == PLAYER:
                    raise RuntimeError(f"host_opened_player (player={PLAYER}, host={host})")
                if host == prize:
                    raise RuntimeError(f"host_opened_prize (prize={prize}, host={host})")
                if prize != PLAYER and host != 3 - prize:
                    raise RuntimeError(f"wrong_host_choice (prize={prize}, host={host})")
                if prize == PLAYER and host not in (1, 2):
                    raise RuntimeError(f"wrong_tie_break (prize={prize}, host={host})")

            # Score both strategies from this round
            if prize == PLAYER:
                stay_win += 1
                switch_lose += 1
            else:
                switch_win += 1
                stay_lose += 1

            sim_counter += 1

    except KeyboardInterrupt:
        # Clean abort: report partial results
        print(f"\nInterrupted at {sim_counter:,} / {sim_target:,} simulations. Reporting partial results…")
        print_report(stay_win, stay_lose, switch_win, switch_lose, sim_counter, args.seed)
        return

    # Finished normally: report full results
    print_report(stay_win, stay_lose, switch_win, switch_lose, sim_target, args.seed)

if __name__ == "__main__":
    main()
