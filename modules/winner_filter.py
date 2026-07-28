def build_winner_set(lotto_df):

    print("\n=== COLUMNS ===")
    print(lotto_df.columns.tolist())
    print("===============")

    winners = set()

    ...

    number_cols = [
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6"
    ]

    for _, row in lotto_df.iterrows():

        combo = tuple(
            sorted(
                int(row[col])
                for col in number_cols
            )
        )

        winners.add(combo)

    return winners


def is_past_winner(
    numbers,
    winner_set
):

    return (
        tuple(sorted(numbers))
        in winner_set
    )

def historical_penalty(
    numbers,
    lotto_df
):

    candidate = set(numbers)

    penalty = 0

    number_cols = [
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6"
    ]

    for _, row in lotto_df.iterrows():

        winner = {
            int(row["번호1"]),
            int(row["번호2"]),
            int(row["번호3"]),
            int(row["번호4"]),
            int(row["번호5"]),
            int(row["번호6"])
        }

        hit = len(
            candidate & winner
        )

        if hit >= 5:

            penalty += 50

        elif hit == 4:

            penalty += 10

    return penalty