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

import json


def load_pair_cache():

    with open(
        "data/pair_cache.json",
        "r",
        encoding="utf-8"
    ) as f:

        raw_cache = json.load(f)

    pair_cache = {}

    for key, value in raw_cache.items():

        pair = tuple(
            int(x)
            for x in key.split("-") 
        )

        pair_cache[pair] = value

    return pair_cache