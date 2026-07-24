import json


def load_triple_cache(
    filename="data/triple_cache.json"
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