import json

from modules.triple_engine import (
    build_triple_frequency
)


def save_triple_cache(
    lotto_df,
    filename="data/triple_cache.json"
):

    triple_counter = build_triple_frequency(
        lotto_df
    )

    data = {
        f"{a}-{b}-{c}": count
        for (a, b, c), count
        in triple_counter.items()
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