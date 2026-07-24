import random

from modules.score_engine import (
    calculate_score
)

from modules.adaptive_engine import (
    get_adaptive_weights
)

from modules.evolution_engine import (
    select_parents,
    create_next_generation
)

from modules.pair_loader import (
    load_pair_cache
)

from modules.pair_engine import (
    calculate_pair_score
)

from modules.triple_loader import (
    load_triple_cache
)

from modules.triple_engine import (
    calculate_triple_score
)

# -------------------------
# LAI 실험 옵션
# -------------------------

USE_ADAPTIVE = False
USE_EVOLUTION = False
USE_PAIR_ENGINE = True
USE_TRIPLE_ENGINE = True

PRIMES = {
    2, 3, 5, 7,
    11, 13, 17, 19,
    23, 29, 31, 37,
    41, 43
}

def create_number_set():

    numbers = random.sample(
        range(1, 46),
        6
    )

    numbers.sort()

    return numbers


def odd_even_check(numbers):

    odd = sum(
        n % 2 == 1
        for n in numbers
    )

    even = 6 - odd

    return (
        (odd == 3 and even == 3)
        or
        (odd == 4 and even == 2)
        or
        (odd == 2 and even == 4)
    )


def low_high_check(numbers):

    low = sum(
        n <= 22
        for n in numbers
    )

    high = 6 - low

    return (
        (low == 3 and high == 3)
        or
        (low == 4 and high == 2)
        or
        (low == 2 and high == 4)
    )


def end_sum_check(numbers):

    end_sum = sum(
        n % 10
        for n in numbers
    )

    return 20 <= end_sum <= 35


def prime_check(numbers):

    primes = {
        2, 3, 5, 7,
        11, 13, 17, 19,
        23, 29, 31, 37,
        41, 43
    }

    prime_count = sum(
        n in primes
        for n in numbers
    )

    return 1 <= prime_count <= 4


def exclude_check(
    numbers,
    exclude_numbers
):

    return len(
        set(numbers) &
        set(exclude_numbers)
    ) == 0


def include_check(
    numbers,
    include_numbers
):

    count = len(
        set(numbers) &
        set(include_numbers)
    )

    return count >= 2

def adaptive_score(
    numbers,
    weights
):

    if not weights:
        return 0

    score = 0

    odd = sum(
        n % 2 == 1
        for n in numbers
    )

    even = 6 - odd

    score += weights.get(
        "odd_even",
        {}
    ).get(
        f"{odd}:{even}",
        0
    )

    low = sum(
        n <= 22
        for n in numbers
    )

    high = 6 - low

    score += weights.get(
        "low_high",
        {}
    ).get(
        f"{low}:{high}",
        0
    )

    prime_count = sum(
        n in PRIMES
        for n in numbers
    )

    score += weights.get(
        "prime",
        {}
    ).get(
        str(prime_count),
        0
    )

    end_sum = sum(
        n % 10
        for n in numbers
    )

    bucket = (
        end_sum // 5
    ) * 5

    score += weights.get(
        "endsum",
        {}
    ).get(
        str(bucket),
        0
    )

    return round(score, 2)


def generate_numbers(
    exclude_numbers,
    include_numbers,
    hot_numbers,
    missing_numbers,
    count=10,
    use_adaptive=True
):

    results = []

    adaptive_weights = get_adaptive_weights()

    pair_cache = load_pair_cache()

    triple_cache = load_triple_cache()

    candidate_count = count * 100

    attempts = 0

    while len(results) < candidate_count:

        attempts += 1

        if attempts > 50000:
            break

        numbers = create_number_set()

        if not odd_even_check(numbers):
            continue

        if not low_high_check(numbers):
            continue

        if not end_sum_check(numbers):
            continue

        if not prime_check(numbers):
            continue

        if not exclude_check(
            numbers,
            exclude_numbers
        ):
            continue

        if not include_check(
            numbers,
            include_numbers
        ):
            continue

        if numbers not in [
            item["numbers"]
            for item in results
        ]:

            base_score = calculate_score(
                numbers,
                include_numbers,
                hot_numbers,
                missing_numbers
            )

            pair_score = calculate_pair_score(
                numbers,
                pair_cache
            )

            triple_score = calculate_triple_score(
                numbers,
                triple_cache
            )

            if USE_ADAPTIVE:

                adaptive = adaptive_score(
                    numbers,
                    adaptive_weights
                )

                score = round(
                    (
                        base_score * 0.9
                        +
                        adaptive * 0.1
                    ),
                    2
                )

            else:

                if USE_PAIR_ENGINE:

                    score = (
                        base_score
                        + (pair_score * 0.01)
                    )

                    if USE_TRIPLE_ENGINE:

                        score += (
                            triple_score * 0.001
                        )

                else:

                    score = base_score

            results.append(
                {
                    "numbers": numbers,
                    "score": score
                }
            )

    # =========================
    # Evolution Generator
    # =========================

    if USE_EVOLUTION:

        elite = select_parents(
            results,
            top_n=min(50, len(results))
        )

        next_generation = create_next_generation(
            elite,
            offspring_count=200
        )

        for numbers in next_generation:

            base_score = calculate_score(
                numbers,
                include_numbers,
                hot_numbers,
                missing_numbers
            )

            pair_score = calculate_pair_score(
                numbers,
                pair_cache
            )

            triple_score = calculate_triple_score(
                numbers,
                triple_cache
            )

            if USE_ADAPTIVE:

                adaptive = adaptive_score(
                    numbers,
                    adaptive_weights
                )

                score = round(
                    (
                        base_score * 0.95
                        +
                        adaptive * 0.05
                    ),
                    2
                )

            else:

                score = (
                    base_score
                    + (pair_score * 0.01)
                )

                if USE_TRIPLE_ENGINE:

                    score += (
                        triple_score * 0.001
                    )

            results.append(
                {
                    "numbers": numbers,
                    "score": score
                }
            )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:count]

print("V2.5 number_generator loaded")