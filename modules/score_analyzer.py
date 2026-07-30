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

        base_score = (
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
                base_score,
                pair_score,
                triple_score,
                core_bonus,
                window_score
            )
        )

        print(
            f"Base={base_score:.2f} "
            f"Pair={pair_score:.2f} "
            f"Triple={triple_score:.2f} "
            f"Core={core_bonus:.2f} "
            f"Window={window_score:.2f}"
        )

        lai_score = 0

        lai_score += max(
            0,
            20 - abs(base_score - 51.41)
        )

        lai_score += max(
            0,
            30 - (
                abs(pair_score - 294.33) / 2
            )
        )

        lai_score += max(
            0,
            30 - abs(triple_score - 54.09)
        )

        lai_score += max(
            0,
            20 - abs(window_score - 13.70)
        )

        results.append({

            "회차":
            row["회차"],

            "base":
            detail["base"],

            "pair":
            detail["pair"],

            "triple":
            detail["triple"],

            "core":
            detail["core"],

            "window":
            detail["window"],

            "total":
            detail["total"],

            "lai_score":
            round(
                lai_score,
                2
            )
        })

    df = pd.DataFrame(
        results
    )

    print(
        "Base Mean =",
        round(df["base"].mean(), 2)
    )

    print(
        "Base Min =",
        round(df["base"].min(), 2)
    )

    print(
        "Base Max =",
        round(df["base"].max(), 2)
    )

    print(
        "평균:",
        round(
            df["total"].mean(),
            2
        )
    )

    top20 = (
        df.sort_values(
            "total",
            ascending=False
        )
        .head(
            int(len(df) * 0.2)
        )
    )

    bottom20 = (
        df.sort_values(
            "total",
            ascending=True
        )
        .head(
            int(len(df) * 0.2)
        )
    )

    print(
        "\n=== 상위20% 평균 ==="
    )

    print(
        top20[
            [
                "base",
                "pair",
                "triple",
                "window"
            ]
        ].mean()
    )

    print(
        "\n=== 하위20% 평균 ==="
    )

    print(
        bottom20[
            [
                "base",
                "pair",
                "triple",
                "window"
            ]
        ].mean()
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
            df["total"].mean(), 2
        ),
        
        "최소": round(
            df["total"].min(), 2
        ),

        "최대": round(
            df["total"].max(), 2
        ),

        "중앙값": round(
            df["total"].median(), 2
        ),
        
        "Base평균": round(
            df["base"].mean(), 2
        ),

        "Pair평균": round(
            df["pair"].mean(), 2
        ),

        "Triple평균": round(
            df["triple"].mean(), 2
        ),

        "Window평균": round(
            df["window"].mean(), 2
        ),

        "Base_10": round(
            df["base"].quantile(0.10), 2
        ),

        "Base_90": round(
            df["base"].quantile(0.90), 2
        ),

        "Pair_10": round(
            df["pair"].quantile(0.10), 2
        ),

        "Pair_90": round(
            df["pair"].quantile(0.90), 2
        ),

        "Triple_10": round(
            df["triple"].quantile(0.10), 2
        ),

        "Triple_90": round(
            df["triple"].quantile(0.90), 2
        ),

        "Window_10": round(
            df["window"].quantile(0.10), 2
        ),

        "Window_90": round(
            df["window"].quantile(0.90), 2
        ),

        "상위80%_하한": round(
            df["total"].quantile(0.10),
            2
        ),

        "상위80%_상한": round(
            df["total"].quantile(0.90),
            2
        ),
        
        "LAI평균": round(
            df["lai_score"].mean(),
            2
        ),

        "LAI_10": round(
            df["lai_score"].quantile(0.10),
            2
        ),

        "LAI_90": round(
            df["lai_score"].quantile(0.90),
            2
        ),

        "LAI최소": round(
            df["lai_score"].min(),
            2
        ),

        "LAI최대": round(
            df["lai_score"].max(),
            2
        )
    }

    return df, summary