from collections import Counter
from itertools import combinations


def build_triple_frequency(lotto):

    triple_counter = Counter()

    number_cols = [
        "1열",
        "2열",
        "3열",
        "4열",
        "5열",
        "6열"
    ]

    for _, row in lotto.iterrows():

        nums = sorted(
            int(row[col])
            for col in number_cols
        )

        for triple in combinations(
            nums,
            3
        ):
            triple_counter[triple] += 1

    return triple_counter


def calculate_triple_score(
    numbers,
    triple_cache
):

    score = 0

    for triple in combinations(
        sorted(numbers),
        3
    ):

        triple_key = "-".join(
            map(str, triple)
        )

        score += triple_cache.get(
            triple_key,
            0
        )

    return score

import pickle
import pandas as pd


def rebuild_triple_cache():

    lotto = pd.read_excel(
        "data/lotto_history.xlsx"
    )

    triple_counter = build_triple_frequency(
        lotto
    )

    triple_cache = {}

    for triple, count in triple_counter.items():

        key = "-".join(
            map(str, triple)
        )

        triple_cache[key] = count

    with open(
        "data/triple_cache.pkl",
        "wb"
    ) as f:

        pickle.dump(
            triple_cache,
            f
        )