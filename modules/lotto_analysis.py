import pandas as pd

from modules.lotto_db import (
    get_lotto_history
)


def get_recent_df(
    lotto=None,
    recent_count=20
):


    if lotto is None:
        lotto = get_lotto_history()

    recent_lotto = lotto.tail(recent_count)

    number_cols = [
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6"
    ]

    recent_numbers = []

    for col in number_cols:

        recent_numbers.extend(
            recent_lotto[col]
            .dropna()
            .astype(int)
            .tolist()
        )

    recent_freq = (
        pd.Series(recent_numbers)
        .value_counts()
    )

    recent_df = pd.DataFrame({
        "번호": recent_freq.index,
        "최근출현횟수": recent_freq.values
    })

    recent_df = recent_df.sort_values(
        "최근출현횟수",
        ascending=False
    )

    return recent_df


def get_missing_df(
    lotto=None
):

    if lotto is None:
        lotto = get_lotto_history()

    number_cols = [
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6"
    ]

    missing_data = []

    for num in range(1, 46):

        miss_count = 0

        for i in range(
            len(lotto)-1,
            -1,
            -1
        ):

            row = lotto.iloc[i]

            numbers = []

            try:

                for col in number_cols:

                    numbers.append(
                        int(row[col])
                    )

            except:
                continue

            if num in numbers:
                break

            miss_count += 1

        missing_data.append(
            [num, miss_count]
        )

    missing_df = pd.DataFrame(
        missing_data,
        columns=[
            "번호",
            "미출현회수"
        ]
    )

    missing_df = missing_df.sort_values(
        "미출현회수",
        ascending=False
    )

    return missing_df