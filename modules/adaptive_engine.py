import pandas as pd
import json

from pathlib import Path

ADAPTIVE_WEIGHTS = None

WEIGHT_FILE = Path(
    "data/adaptive_weights.json"
)

NUMBER_COLS = [
    "번호1",
    "번호2",
    "번호3",
    "번호4",
    "번호5",
    "번호6"
]


PRIMES = [
    2, 3, 5, 7,
    11, 13, 17, 19,
    23, 29, 31, 37,
    41, 43
]


def build_odd_even_weights(lotto):

    patterns = {}

    for _, row in lotto.iterrows():

        try:

            numbers = [
                int(row[col])
                for col in NUMBER_COLS
            ]

            odd = sum(
                n % 2 == 1
                for n in numbers
            )

            even = 6 - odd

            pattern = (
                f"{odd}:{even}"
            )

            patterns[pattern] = (
                patterns.get(
                    pattern,
                    0
                ) + 1
            )

        except:

            pass

    max_count = max(
        patterns.values()
    )

    return {

        k: round(
            v / max_count * 10,
            2
        )

        for k, v
        in patterns.items()

    }


def build_low_high_weights(lotto):

    patterns = {}

    for _, row in lotto.iterrows():

        try:

            numbers = [
                int(row[col])
                for col in NUMBER_COLS
            ]

            low = sum(
                n <= 22
                for n in numbers
            )

            high = 6 - low

            pattern = (
                f"{low}:{high}"
            )

            patterns[pattern] = (
                patterns.get(
                    pattern,
                    0
                ) + 1
            )

        except:

            pass

    max_count = max(
        patterns.values()
    )

    return {

        k: round(
            v / max_count * 10,
            2
        )

        for k, v
        in patterns.items()

    }


def build_prime_weights(lotto):

    counts = {}

    for _, row in lotto.iterrows():

        try:

            numbers = [
                int(row[col])
                for col in NUMBER_COLS
            ]

            prime_count = sum(
                n in PRIMES
                for n in numbers
            )

            counts[prime_count] = (
                counts.get(
                    prime_count,
                    0
                ) + 1
            )

        except:

            pass

    max_count = max(
        counts.values()
    )

    return {

        k: round(
            v / max_count * 10,
            2
        )

        for k, v
        in counts.items()

    }


def build_endsum_weights(lotto):

    groups = {}

    for _, row in lotto.iterrows():

        try:

            numbers = [
                int(row[col])
                for col in NUMBER_COLS
            ]

            end_sum = sum(
                n % 10
                for n in numbers
            )

            bucket = (
                end_sum // 5
            ) * 5

            groups[bucket] = (
                groups.get(
                    bucket,
                    0
                ) + 1
            )

        except:

            pass

    max_count = max(
        groups.values()
    )

    return {

        k: round(
            v / max_count * 10,
            2
        )

        for k, v
        in groups.items()

    }


def initialize_adaptive_weights(
    lotto
):

    global ADAPTIVE_WEIGHTS

    ADAPTIVE_WEIGHTS = {

        "odd_even":
        build_odd_even_weights(
            lotto
        ),

        "low_high":
        build_low_high_weights(
            lotto
        ),

        "prime":
        build_prime_weights(
            lotto
        ),

        "endsum":
        build_endsum_weights(
            lotto
        )

    }

    save_adaptive_weights()

    return ADAPTIVE_WEIGHTS


def get_adaptive_weights():

    global ADAPTIVE_WEIGHTS

    if ADAPTIVE_WEIGHTS is None:

        load_adaptive_weights()

    return ADAPTIVE_WEIGHTS

def save_adaptive_weights():

    global ADAPTIVE_WEIGHTS

    if ADAPTIVE_WEIGHTS is None:

        return

    with open(
        WEIGHT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            ADAPTIVE_WEIGHTS,
            f,
            ensure_ascii=False,
            indent=4
        )

def load_adaptive_weights():

    global ADAPTIVE_WEIGHTS

    if not WEIGHT_FILE.exists():

        return None

    with open(
        WEIGHT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        ADAPTIVE_WEIGHTS = json.load(
            f
        )

    return ADAPTIVE_WEIGHTS