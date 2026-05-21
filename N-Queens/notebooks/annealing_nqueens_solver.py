import math
import random
import time
import tracemalloc
from nqueens_utils import RunResult, count_conflicts

DEFAULT_SEED = 42


def conflicted_rows(board: list[int]) -> list[int]:
    n = len(board)
    rows: list[int] = []
    for row, col in enumerate(board):
        clashes = 0
        for other_row, other_col in enumerate(board):
            if other_row == row:
                continue
            if abs(other_col - col) == abs(other_row - row):
                clashes += 1
        if clashes:
            rows.append(row)
    return rows


def local_repair(board: list[int], rng: random.Random, max_steps: int) -> tuple[list[int], bool, int]:
    candidate = board[:]
    n = len(candidate)

    for step in range(1, max_steps + 1):
        current_conflicts = count_conflicts(candidate)
        if current_conflicts == 0:
            return candidate, True, step - 1

        rows = conflicted_rows(candidate)
        if not rows:
            return candidate, True, step - 1

        row = rng.choice(rows)
        best_score = None
        best_swap_row = row

        for other_row in range(n):
            if other_row == row:
                continue
            candidate[row], candidate[other_row] = candidate[other_row], candidate[row]
            score = count_conflicts(candidate)
            candidate[row], candidate[other_row] = candidate[other_row], candidate[row]

            if best_score is None or score < best_score:
                best_score = score
                best_swap_row = other_row

        candidate[row], candidate[best_swap_row] = candidate[best_swap_row], candidate[row]

    return candidate, count_conflicts(candidate) == 0, max_steps


def solve_simulated_annealing(n: int, seed: int = DEFAULT_SEED) -> tuple[list[int] | None, bool, int, str]:
    if n in (2, 3):
        return None, False, 0, "No valid solution exists for N = 2 or N = 3."

    rng = random.Random(seed)
    max_restarts = 4
    max_steps = max(5000, 300 * n)
    cooling_rate = 0.9995
    initial_temperature = max(25.0, n * 0.4)
    total_steps = 0
    best_board: list[int] | None = None
    best_conflicts = float("inf")

    for restart in range(max_restarts):
        board = list(range(n))
        rng.shuffle(board)
        temperature = initial_temperature
        current_conflicts = count_conflicts(board)

        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            best_board = board[:]

        for _ in range(max_steps):
            total_steps += 1
            if current_conflicts == 0:
                return board[:], True, total_steps, f"Solved with simulated annealing after {restart} restart(s)."

            first_row, second_row = rng.sample(range(n), 2)
            board[first_row], board[second_row] = board[second_row], board[first_row]
            next_conflicts = count_conflicts(board)
            delta = next_conflicts - current_conflicts

            if delta <= 0 or rng.random() < math.exp(-delta / max(temperature, 1e-9)):
                current_conflicts = next_conflicts
                if current_conflicts < best_conflicts:
                    best_conflicts = current_conflicts
                    best_board = board[:]
            else:
                board[first_row], board[second_row] = board[second_row], board[first_row]

            temperature *= cooling_rate

    if best_board is not None:
        repaired_board, repaired, repair_steps = local_repair(best_board, rng, max_steps=max(200, 10 * n))
        if repaired:
            total_steps += repair_steps
            return repaired_board, True, total_steps, "Solved after annealing plus final local repair."
        best_board = repaired_board[:]
        best_conflicts = count_conflicts(repaired_board)

    final_note = f"Annealing stopped after {max_restarts} restart(s); best board had {int(best_conflicts)} conflict(s)."
    return best_board, False, total_steps, final_note


def run_case(n: int) -> RunResult:
    tracemalloc.start()
    start_time = time.perf_counter()
    solution, solved, steps, note = solve_simulated_annealing(n)
    elapsed = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    conflicts = count_conflicts(solution) if solution is not None else "N/A"
    status = "SOLVED" if solved else "FAILED"

    print(f"[Annealing] N={n} | Status={status} | Steps={steps} | Conflicts={conflicts} | Time={elapsed:.4f}s | Memory={peak / (1024*1024):.4f}MB")

    return RunResult(
        n=n,
        status=status,
        solved=solved,
        steps=steps,
        conflicts=conflicts,
        time_seconds=elapsed,
        memory_mb=peak / (1024 * 1024),
        note=note,
        solution=solution,
    )
