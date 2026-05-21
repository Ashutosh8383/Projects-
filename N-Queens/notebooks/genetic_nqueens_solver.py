import random
import time
import tracemalloc
from nqueens_utils import RunResult, count_conflicts

DEFAULT_SEED = 42


def fitness(board: list[int]) -> int:
    n = len(board)
    max_pairs = n * (n - 1) // 2
    return max_pairs - count_conflicts(board)


def order_crossover(parent_one: list[int], parent_two: list[int], rng: random.Random) -> tuple[list[int], list[int]]:
    size = len(parent_one)
    left, right = sorted(rng.sample(range(size), 2))

    def build_child(first: list[int], second: list[int]) -> list[int]:
        child = [-1] * size
        child[left : right + 1] = first[left : right + 1]
        fill_values = [value for value in second if value not in child]
        fill_index = 0
        for index in range(size):
            if child[index] == -1:
                child[index] = fill_values[fill_index]
                fill_index += 1
        return child

    return build_child(parent_one, parent_two), build_child(parent_two, parent_one)


def mutate(board: list[int], rng: random.Random, mutation_rate: float) -> None:
    if rng.random() >= mutation_rate:
        return
    first, second = rng.sample(range(len(board)), 2)
    board[first], board[second] = board[second], board[first]


def solve_genetic(n: int, seed: int = DEFAULT_SEED) -> tuple[list[int] | None, bool, int, str]:
    if n in (2, 3):
        return None, False, 0, "No valid solution exists for N = 2 or N = 3."

    rng = random.Random(seed)
    population_size = 60 if n >= 100 else 80
    generations = 350 if n >= 200 else 500 if n >= 100 else 700
    elite_size = max(6, population_size // 10)
    mutation_rate = 0.20 if n >= 100 else 0.14
    population = [rng.sample(range(n), n) for _ in range(population_size)]
    best_board: list[int] | None = None
    best_conflicts = float("inf")

    for generation in range(1, generations + 1):
        population.sort(key=fitness, reverse=True)
        current_best = population[0]
        current_conflicts = count_conflicts(current_best)

        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            best_board = current_best[:]

        if current_conflicts == 0:
            return current_best[:], True, generation, "Solved using the genetic algorithm."

        next_population = [candidate[:] for candidate in population[:elite_size]]

        while len(next_population) < population_size:
            parent_one = max(rng.sample(population, min(4, len(population))), key=fitness)
            parent_two = max(rng.sample(population, min(4, len(population))), key=fitness)
            child_one, child_two = order_crossover(parent_one, parent_two, rng)
            mutate(child_one, rng, mutation_rate)
            mutate(child_two, rng, mutation_rate)
            next_population.append(child_one)
            if len(next_population) < population_size:
                next_population.append(child_two)

        population = next_population

    final_note = f"Reached generation limit; best board had {int(best_conflicts)} conflict(s)."
    return best_board, False, generations, final_note


def run_case(n: int) -> RunResult:
    tracemalloc.start()
    start_time = time.perf_counter()
    solution, solved, steps, note = solve_genetic(n)
    elapsed = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    conflicts = count_conflicts(solution) if solution is not None else "N/A"
    status = "SOLVED" if solved else "FAILED"

    print(f"[Genetic] N={n} | Status={status} | Generations={steps} | Conflicts={conflicts} | Time={elapsed:.4f}s | Memory={peak / (1024*1024):.4f}MB")

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
