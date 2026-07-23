import pandas as pd


def train_odd_even_weights(
    result_df
):

    pattern_hits = {}

    for _, row in result_df.iterrows():

        pattern = row["홀짝패턴"]

        hit = row["적중수"]

        if pattern not in pattern_hits:

            pattern_hits[pattern] = []

        pattern_hits[pattern].append(
            hit
        )

    max_avg = max(
        sum(v) / len(v)
        for v in pattern_hits.values()
    )

    weights = {}

    for pattern, hits in pattern_hits.items():

        avg_hit = (
            sum(hits)
            /
            len(hits)
        )

        weights[pattern] = round(
            avg_hit
            /
            max_avg
            * 10,
            2
        )

    return weights


def train_low_high_weights(
    result_df
):

    pattern_hits = {}

    for _, row in result_df.iterrows():

        pattern = row["저고패턴"]

        hit = row["적중수"]

        if pattern not in pattern_hits:

            pattern_hits[pattern] = []

        pattern_hits[pattern].append(
            hit
        )

    max_avg = max(
        sum(v) / len(v)
        for v in pattern_hits.values()
    )

    weights = {}

    for pattern, hits in pattern_hits.items():

        avg_hit = (
            sum(hits)
            /
            len(hits)
        )

        weights[pattern] = round(
            avg_hit
            /
            max_avg
            * 10,
            2
        )

    return weights


def train_prime_weights(
    result_df
):

    pattern_hits = {}

    for _, row in result_df.iterrows():

        pattern = str(
            row["소수개수"]
        )

        hit = row["적중수"]

        if pattern not in pattern_hits:

            pattern_hits[pattern] = []

        pattern_hits[pattern].append(
            hit
        )

    max_avg = max(
        sum(v) / len(v)
        for v in pattern_hits.values()
    )

    weights = {}

    for pattern, hits in pattern_hits.items():

        avg_hit = (
            sum(hits)
            /
            len(hits)
        )

        weights[pattern] = round(
            avg_hit
            /
            max_avg
            * 10,
            2
        )

    return weights


def train_endsum_weights(
    result_df
):

    pattern_hits = {}

    for _, row in result_df.iterrows():

        bucket = str(
            row["끝수합구간"]
        )

        hit = row["적중수"]

        if bucket not in pattern_hits:

            pattern_hits[bucket] = []

        pattern_hits[bucket].append(
            hit
        )

    max_avg = max(
        sum(v) / len(v)
        for v in pattern_hits.values()
    )

    weights = {}

    for bucket, hits in pattern_hits.items():

        avg_hit = (
            sum(hits)
            /
            len(hits)
        )

        weights[bucket] = round(
            avg_hit
            /
            max_avg
            * 10,
            2
        )

    return weights


def train_all_weights(
    result_df
):

    return {

        "odd_even":
        train_odd_even_weights(
            result_df
        ),

        "low_high":
        train_low_high_weights(
            result_df
        ),

        "prime":
        train_prime_weights(
            result_df
        ),

        "endsum":
        train_endsum_weights(
            result_df
        )

    }