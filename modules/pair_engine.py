from itertools import combinations
from collections import Counter


def build_pair_frequency(lotto_df):

    pair_counter = Counter()

    number_cols = [
        "1열",
        "2열",
        "3열",
        "4열",
        "5열",
        "6열"
    ]

    for _, row in lotto_df.iterrows():

        numbers = sorted([
            row[col]
            for col in number_cols
        ])

        pairs = combinations(
            numbers,
            2
        )

        pair_counter.update(pairs)

    return pair_counter


def calculate_pair_score(
    numbers,
    pair_counter
):

    score = 0

    for pair in combinations(
        sorted(numbers),
        2
    ):

        score += pair_counter.get(
            pair,
            0
        )

    return score

import pickle
import pandas as pd

def rebuild_pair_cache():

    lotto = pd.read_excel(
        "data/lotto_history.xlsx"
    )

    pair_counter = build_pair_frequency(
        lotto
    )

    with open(
        "data/pair_cache.pkl",
        "wb"
    ) as f:

        pickle.dump(
            pair_counter,
            f
        )