import sys
import time
import tracemalloc
from nqueens_utils import RunResult, count_conflicts


def solve_dfs(n: int, time_limit: float = 15.0) -> tuple[list[int] | None, bool, int, str]:
    if n in (2, 3):
        return None, False, 0, "No valid solution exists for N = 2 or N = 3."

    sys.setrecursionlimit(max(2000, n + 100))
    full_mask = (1 << n) - 1
    solution = [-1] * n
    steps = 0
    started_at = time.perf_counter()

    def backtrack(row: int, columns: int, diag_left: int, diag_right: int) -> bool:
        nonlocal steps
        steps += 1

        if steps % 2048 == 0 and time.perf_counter() - started_at > time_limit:
            return False

        if row == n:
            return True

        available = full_mask & ~(columns | diag_left | diag_right)

        while available:
            bit = available & -available
            available ^= bit
            col = bit.bit_length() - 1
            solution[row] = col

            if backtrack(
                row + 1,
                columns | bit,
                ((diag_left | bit) << 1) & full_mask,
                (diag_right | bit) >> 1,
            ):
                return True

            if time.perf_counter() - started_at > time_limit:
                return False

        solution[row] = -1
        return False

    solved = backtrack(0, 0, 0, 0)
    elapsed = time.perf_counter() - started_at

    if solved and -1 not in solution:
        return solution[:], True, steps, "Solved with full exhaustive backtracking."

    if elapsed > time_limit:
        return None, False, steps, f"Stopped after reaching the {time_limit:.0f}s time limit."

    return None, False, steps, "Search finished without locating a solution."


def run_case(n: int) -> RunResult:
    tracemalloc.start()
    start_time = time.perf_counter()
    solution, solved, steps, note = solve_dfs(n)
    elapsed = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    conflicts = count_conflicts(solution) if solution is not None else "N/A"
    status = "SOLVED" if solved else "TIMEOUT" if "time limit" in note.lower() else "FAILED"

    print(f"[DFS] N={n} | Status={status} | Steps={steps} | Conflicts={conflicts} | Time={elapsed:.4f}s | Memory={peak / (1024*1024):.4f}MB")

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
