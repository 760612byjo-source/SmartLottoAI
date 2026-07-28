import pandas as pd

from modules.lotto_analysis import (
    get_recent_df,
    get_missing_df
)

from modules.exclude_engine import (
    calculate_excluded_numbers
)

from modules.include_engine import (
    calculate_included_numbers
)

from modules.number_generator import (
    generate_numbers
)


def count_matches(
    predicted,
    actual
):

    return len(
        set(predicted)
        &
        set(actual)
    )


def run_backtest(
    lotto,
    start_idx=100,
    game_count=5,
    use_adaptive=True
):


    results = []

    for target_idx in range(
        start_idx,
        len(lotto)
    ):

        history = lotto.iloc[
            :target_idx
        ].copy()

        actual_row = lotto.iloc[
            target_idx
        ]

        recent_df = get_recent_df(
            history
        )

        missing_df = get_missing_df(
            history
        )

        exclude_df = (
            calculate_excluded_numbers(
                recent_df,
                missing_df
            )
        )

        include_df = (
            calculate_included_numbers(
                recent_df,
                missing_df
            )
        )

        exclude_numbers = (
            exclude_df.head(10)["번호"]
            .astype(int)
            .tolist()
        )

        include_numbers = (
            include_df.head(10)["번호"]
            .astype(int)
            .tolist()
        )

        hot_numbers = (
            recent_df.head(10)["번호"]
            .astype(int)
            .tolist()
        )

        missing_numbers = (
            missing_df.head(10)["번호"]
            .astype(int)
            .tolist()
        )

        generated = generate_numbers(
            exclude_numbers,
            include_numbers,
            hot_numbers,
            missing_numbers,
            game_count,
            use_adaptive
        )

        actual_numbers = [

            int(actual_row["번호1"]),
            int(actual_row["번호2"]),
            int(actual_row["번호3"]),
            int(actual_row["번호4"]),
            int(actual_row["번호5"]),
            int(actual_row["번호6"])

        ]

        best_hit = 0

        best_numbers = []

        for item in generated:

            hit = count_matches(
                item["numbers"],
                actual_numbers
            )

            if hit > best_hit:

                best_hit = hit
                best_numbers = item["numbers"]

        odd_count = sum(
            n % 2 == 1
            for n in best_numbers
        )

        even_count = 6 - odd_count

        low_count = sum(
            n <= 22
            for n in best_numbers
        )

        high_count = 6 - low_count

        PRIMES = [
            2, 3, 5, 7,
            11, 13, 17, 19,
            23, 29, 31, 37,
            41, 43
        ]

        prime_count = sum(
            n in PRIMES
            for n in best_numbers
        )

        end_sum = sum(
            n % 10
            for n in best_numbers
        )

        end_bucket = (
            end_sum // 5
        ) * 5

        group1 = sum(
            1 <= n <= 15
            for n in best_numbers
        )
                            
        group2 = sum(
            16 <= n <= 30
            for n in best_numbers
        )
                            
        group3 = sum(
            31 <= n <= 45
            for n in best_numbers
        )
                            
        group_pattern = (
            f"{group1}:{group2}:{group3}"
        )

        results.append({

            "회차": int(
                actual_row["회차"]
            ),

            "적중수": best_hit,

            "홀짝패턴":
            f"{odd_count}:{even_count}",

            "저고패턴":
            f"{low_count}:{high_count}",

            "소수개수":
            prime_count,

            "끝수합구간":
            end_bucket,

            "예측번호":
            ", ".join(
                map(str, best_numbers)
            ),

            "당첨번호":
            ", ".join(
                map(str, actual_numbers)
            ),

            "삼그룹패턴":
            group_pattern        

        })

    return pd.DataFrame(
        results
    )