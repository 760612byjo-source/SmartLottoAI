import os
import pandas as pd
from datetime import datetime

HISTORY_FILE = (
    "data/recommendation_history.csv"
)


def save_recommendation(numbers):

    row = {

        "created_at":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "numbers":
        ",".join(
            map(str, numbers)
        )
    }

    if os.path.exists(
        HISTORY_FILE
    ):

        df = pd.read_csv(
            HISTORY_FILE
        )

        df = pd.concat(
            [
                df,
                pd.DataFrame([row])
            ],
            ignore_index=True
        )

    else:

        df = pd.DataFrame(
            [row]
        )

    df.to_csv(
        HISTORY_FILE,
        index=False,
        encoding="utf-8-sig"
    )


def load_recommendations():

    if not os.path.exists(
        HISTORY_FILE
    ):

        return pd.DataFrame(
            columns=[
                "created_at",
                "numbers"
            ]
        )

    return pd.read_csv(
        HISTORY_FILE
    )


def delete_all_recommendations():

    if os.path.exists(
        HISTORY_FILE
    ):

        os.remove(
            HISTORY_FILE
        )

def delete_recommendation(index):

    df = pd.read_csv(
        HISTORY_FILE
    )

    df = df.drop(index)

    df.to_csv(
        HISTORY_FILE,
        index=False,
        encoding="utf-8-sig"
    )