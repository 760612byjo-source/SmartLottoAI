from itertools import combinations
from collections import Counter


def build_pair_frequency(lotto_df):

    pair_counter = Counter()

    number_cols = [
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6"
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