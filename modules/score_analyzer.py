import pandas as pd

from modules.score_engine import (
    calculate_score
)

from modules.pair_engine import (
    calculate_pair_score,
    load_pair_cache     
)

from modules.triple_engine import (
    calculate_triple_score,
    load_triple_cache
)

from modules.window_pattern_engine import (
    build_window_patterns,
    calculate_window_pattern_score
)

from modules.number_generator import (
    calculate_score_detail
)


NUMBER_COLS = [
    "번호1",
    "번호2",
    "번호3",
    "번호4",
    "번호5",
    "번호6"
]


def analyze_winner_scores(
    lotto_df
):

    pair_cache = load_pair_cache()

    triple_cache = load_triple_cache()

    window_patterns = (
        build_window_patterns(
            lotto_df
        )
    )

    results = []

    for _, row in lotto_df.iterrows():

        numbers = [

            int(row[col])

            for col in NUMBER_COLS

        ]

        adaptive_score = (
            calculate_score(
                numbers,
                [],
                [],
                []
            )
        )

        pair_score = (
                calculate_pair_score(
                    numbers,
                    pair_cache
                )
            )
        
        triple_score = (
            calculate_triple_score(
                numbers,
                triple_cache
            )
        )

        core_bonus = 0

        window_score = (
            calculate_window_pattern_score(
                numbers,
                window_patterns
            )
        )

        detail = (
            calculate_score_detail(
                adaptive_score,
                pair_score,
                triple_score,
                core_bonus,
                window_score
            )
        )

        print(
            f"Adaptive={adaptive_score:.2f} "
            f"Pair={pair_score:.2f} "
            f"Triple={triple_score:.2f} "
            f"Core={core_bonus:.2f} "
            f"Window={window_score:.2f}"
        )

        results.append({

            "회차":
            row["회차"],

            "adaptive":
            detail["adaptive"],

            "pair":
            detail["pair"],

            "triple":
            detail["triple"],

            "core":
            detail["core"],

            "window":
            detail["window"],

            "total":
            detail["total"]
        })

    df = pd.DataFrame(
        results
    )

    print(
        "평균:",
        round(
            df["total"].mean(),
            2
        )
    )

    print(
        "최소:",
        round(
            df["total"].min(),
            2
        )
    )

    print(
        "최대:",
        round(
            df["total"].max(),
            2
        )
    )

    summary = {

        "평균": round(
            df["total"].mean(),
            2
        ),

        "최소": round(
            df["total"].min(),
            2
        ),

        "최대": round(
            df["total"].max(),
            2
        ),

        "중앙값": round(
            df["total"].median(),
            2
        ),

        "상위80%_하한": round(
            df["total"].quantile(0.10),
            2
        ),

        "상위80%_상한": round(
            df["total"].quantile(0.90),
            2
        )
    }

    return df, summary