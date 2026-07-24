import json


def load_pair_cache(
    filename="data/pair_cache.json"
):

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}