import json

from modules.pair_engine import (
    build_pair_frequency
)


def save_pair_cache(
    lotto_df,
    filename="data/pair_cache.json"
):

    pair_counter = build_pair_frequency(
        lotto_df
    )

    data = {
        f"{a}-{b}": count
        for (a, b), count
        in pair_counter.items()
    }

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    return len(data)