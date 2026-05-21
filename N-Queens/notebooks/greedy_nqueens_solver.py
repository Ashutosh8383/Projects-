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


def solve_greedy(n: int, seed: int = DEFAULT_SEED) -> tuple[list[int] | None, bool, int, str]:
    if n in (2, 3):
        return None, False, 0, "No valid solution exists for N = 2 or N = 3."

    rng = random.Random(seed)
    max_steps = max(200, 50 * n)
    max_restarts = 12
    total_steps = 0
    best_board: list[int] | None = None
    best_conflicts = float("inf")

    for restart in range(max_restarts):
        board = [rng.randrange(n) for _ in range(n)]
        col_counts = [0] * n
        diag_main = [0] * (2 * n - 1)
        diag_anti = [0] * (2 * n - 1)

        for row, col in enumerate(board):
            col_counts[col] += 1
            diag_main[row - col + n - 1] += 1
            diag_anti[row + col] += 1

        def row_conflicts(row: int, col: int) -> int:
            return col_counts[col] + diag_main[row - col + n - 1] + diag_anti[row + col] - 3

        for _ in range(max_steps):
            total_steps += 1
            conflicted = [row for row, col in enumerate(board) if row_conflicts(row, col) > 0]

            if not conflicted:
                return board[:], True, total_steps, f"Solved with greedy search after {restart} restart(s)."

            current_conflicts = count_conflicts(board)
            if current_conflicts < best_conflicts:
                best_conflicts = current_conflicts
                best_board = board[:]

            row = rng.choice(conflicted)
            current_col = board[row]
            col_counts[current_col] -= 1
            diag_main[row - current_col + n - 1] -= 1
            diag_anti[row + current_col] -= 1

            best_score = None
            candidate_columns: list[int] = []
            for col in range(n):
                score = col_counts[col] + diag_main[row - col + n - 1] + diag_anti[row + col]
                if best_score is None or score < best_score:
                    best_score = score
                    candidate_columns = [col]
                elif score == best_score:
                    candidate_columns.append(col)

            new_col = rng.choice(candidate_columns)
            board[row] = new_col
            col_counts[new_col] += 1
            diag_main[row - new_col + n - 1] += 1
            diag_anti[row + new_col] += 1

    final_note = f"Stopped after {max_restarts} restart(s); best board had {int(best_conflicts)} conflict(s)."
    return best_board, False, total_steps, final_note


def run_case(n: int) -> RunResult:
    tracemalloc.start()
    start_time = time.perf_counter()
    solution, solved, steps, note = solve_greedy(n)
    elapsed = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    conflicts = count_conflicts(solution) if solution is not None else "N/A"
    status = "SOLVED" if solved else "FAILED"

    print(f"[Greedy] N={n} | Status={status} | Steps={steps} | Conflicts={conflicts} | Time={elapsed:.4f}s | Memory={peak / (1024*1024):.4f}MB")

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
