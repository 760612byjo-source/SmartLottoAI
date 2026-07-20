import pandas as pd


def calculate_included_numbers(
    recent_df,
    missing_df
):

    scores = {}

    for num in range(1, 46):
        scores[num] = 0

    # 최근 강세수
    hot_numbers = (
        recent_df
        .sort_values(
            "최근출현횟수",
            ascending=False
        )
        .head(15)
    )

    for num in hot_numbers["번호"]:
        scores[int(num)] += 3

    # 장기 미출현 제외
    active_numbers = (
        missing_df
        .sort_values(
            "미출현회수"
        )
        .head(20)
    )

    for num in active_numbers["번호"]:
        scores[int(num)] += 2

    include_df = pd.DataFrame({
        "번호": list(scores.keys()),
        "포함점수": list(scores.values())
    })

    include_df = include_df.sort_values(
        "포함점수",
        ascending=False
    )

    return include_df