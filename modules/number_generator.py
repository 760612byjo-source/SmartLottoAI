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

from modules.consensus_engine import (
    get_consensus_numbers,
    get_core_numbers
)

from modules.winner_filter import (
    build_winner_set,
    is_past_winner,
)

from modules.lotto_db import (
    get_lotto_history
)

from modules.window_pattern_engine import (
    build_window_patterns,
    calculate_window_pattern_score
)

# -------------------------
# LAI 실험 옵션
# -------------------------

USE_ADAPTIVE = False
USE_EVOLUTION = False
USE_PAIR_ENGINE = True
USE_TRIPLE_ENGINE = True
WINNER_SET = None
WINDOW_PATTERNS = None

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

    prime_count = sum(
        n in PRIMES
        for n in numbers
    )

    return 1 <= prime_count <= 4

def consecutive_score(numbers):

    score = 0

    numbers = sorted(numbers)

    consecutive = 0

    for i in range(5):

        if numbers[i + 1] - numbers[i] == 1:

            consecutive += 1

    if consecutive == 0:

        score += 3

    elif consecutive == 1:

        score += 1

    elif consecutive >= 3:

        score -= 5

    return score


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

    if not include_numbers:
        return True

    count = len(
        set(numbers) &
        set(include_numbers)
    )

    return count >= 2

def calculate_adaptive_score(
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

def calculate_core_bonus(
    numbers,
    core_numbers
):

    core_match = len(
        set(numbers)
        &
        set(core_numbers)
    )

    if core_match >= 4:
        return 3.0

    elif core_match == 3:
        return 1.5

    elif core_match == 2:
        return 0.5

    return 0


def generate_numbers(
    exclude_numbers,
    include_numbers,
    hot_numbers,
    missing_numbers,
    count=10
):

    results = []

    used_numbers = set()

    adaptive_weights = get_adaptive_weights()

    pair_cache = load_pair_cache()

    triple_cache = load_triple_cache()

    global WINDOW_PATTERNS

    if WINDOW_PATTERNS is None:

        lotto_df = get_lotto_history()

        WINDOW_PATTERNS = (
            build_window_patterns(
                lotto_df
            )
        )

    window_patterns = WINDOW_PATTERNS

    
    core_numbers = (
        hot_numbers[:6]
    )

    candidate_count = count * 70

    attempts = 0

    global WINNER_SET

    if WINNER_SET is None:

        lotto_df = get_lotto_history()

        WINNER_SET = build_winner_set(
            lotto_df
        )

    winner_set = WINNER_SET

    while len(results) < candidate_count:

        attempts += 1

        if attempts > 50000:
            break

        numbers = create_number_set()

        if is_past_winner(
            numbers,
            winner_set
        ):
            continue

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

        numbers_key = tuple(numbers)

        if numbers_key in used_numbers:
            continue

        used_numbers.add(numbers_key)

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

        window_pattern_score = (
            calculate_window_pattern_score(
                numbers,
                window_patterns
            )
        )
            
        if USE_ADAPTIVE:

            adaptive = calculate_adaptive_score(
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

                score = 0

                score += max(
                    0,
                    20 - abs(base_score - 51.41)
                )

                score += max(
                    0,
                    30 - (
                        abs(pair_score - 294.33) / 2
                    )
                )

                score += max(
                    0,
                    30 - abs(triple_score - 54.09)
                )

                score += max(
                    0,
                    20 - abs(window_pattern_score - 13.70)
                )

                core_bonus = calculate_core_bonus(
                    numbers,
                    core_numbers
                )

                score += core_bonus

                score += consecutive_score(
                    numbers
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

            window_pattern_score = (
                calculate_window_pattern_score(
                    numbers,
                    window_patterns
                )
            )

            if USE_ADAPTIVE:

                adaptive = calculate_adaptive_score(
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

                score = 0

                score += max(
                    0,
                    20 - abs(base_score - 51.41)
                )

                score += max(
                    0,
                    30 - (
                        abs(pair_score - 294.33) / 2
                    )
                )

                score += max(
                    0,
                    30 - abs(triple_score - 54.09)
                )

                score += max(
                    0,
                    20 - abs(window_pattern_score - 13.70)
                )

                core_bonus = calculate_core_bonus(
                    numbers,
                    core_numbers
                )

                score += core_bonus

                score += consecutive_score(
                    numbers
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

    score_band_results = [

        item

        for item in results

        if 68 <= item["score"] <= 70

    ]

    print(
        f"68~70 Score Band : "
        f"{len(score_band_results)}"
    )

    all_scores = [
        item["score"]
        for item in results
    ]

    if len(all_scores) == 0:

        print(
            "Generated Score Range : EMPTY"
        )

        return []

    print(
        f"Generated Score Range : "
        f"{min(all_scores):.2f}"
        f" ~ "
        f"{max(all_scores):.2f}"
    )

    print(
        f"Generated Score Avg : "
        f"{sum(all_scores) / len(all_scores):.2f}"
    )

    top_scores = sorted(
        all_scores,
        reverse=True
    )[:20]

    print(
        f"TOP20 Avg : "
        f"{sum(top_scores) / len(top_scores):.2f}"
    )

    print(
        f"Gap : "
        f"{(sum(all_scores) / len(all_scores)) - 57.15:.2f}"
    )

    top_results = apply_diversity_filter(
        results,
        count
    )



    consensus = get_consensus_numbers(
        top_results
    )

    print("\n=== Consensus TOP 10 ===")

    for number, freq in consensus[:10]:

        print(
            f"{number} : {freq}회"
        )

    core_numbers = get_core_numbers(
        top_results,
        top_n=6
    )

    print(
        f"results : {len(results)}"
    )

    print(
        f"top_results : {len(top_results)}"
    )

    print("\n=== TOP RESULTS ===")

    for item in top_results[:10]:

        print(
            item["score"],
            item["numbers"]
        )

    print("\n=== CORE NUMBERS ===")

    print(core_numbers)

    return top_results


print("V2.5 number_generator loaded")

def calculate_score_detail(
    base_score,
    pair_score,
    triple_score,
    core_bonus,
    window_pattern_score
):

    window_score = (
        window_pattern_score
    )

    total_score = (
        base_score
        + pair_score
        + triple_score
        + core_bonus
        + window_score
    )

    return {

        "base": round(
            base_score,
            2
        ),

        "pair": round(
            pair_score,
            2
        ),

        "triple": round(
            triple_score,
            2
        ),

        "core": round(
            core_bonus,
            2
        ),

        "window": round(
            window_score,
            2
        ),

        "total": round(
            total_score,
            2
        )
    }

def apply_diversity_filter(
    results,
    target_count=10
):

    selected = []

    for candidate in results:

        nums = set(
            candidate["numbers"]
        )

        keep = True

        for existing in selected:

            common = len(
                nums &
                set(existing["numbers"])
            )

            if common >= 5:

                keep = False
                break

        if keep:

            selected.append(
                candidate
            )

        if len(selected) >= target_count:

            break

    return selected