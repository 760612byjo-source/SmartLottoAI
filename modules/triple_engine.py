from collections import Counter
from itertools import combinations


def build_triple_frequency(lotto):

    triple_counter = Counter()

    number_cols = [
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6"
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