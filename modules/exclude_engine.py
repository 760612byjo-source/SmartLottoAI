import pandas as pd


def calculate_excluded_numbers(
    recent_df,
    missing_df
):

    scores = {}

    for num in range(1, 46):

        scores[num] = 0

    # 최근출현수 점수
    recent_bottom = (
        recent_df
        .sort_values(
            "최근출현횟수"
        )
        .head(15)
    )

    for num in recent_bottom["번호"]:

        scores[int(num)] += 2

    # 장기 미출현수
    missing_top = (
        missing_df
        .sort_values(
            "미출현회수",
            ascending=False
        )
        .head(15)
    )

    for num in missing_top["번호"]:

        scores[int(num)] += 2

    score_df = pd.DataFrame({
        "번호": list(scores.keys()),
        "제외점수": list(scores.values())
    })

    score_df = score_df.sort_values(
        "제외점수",
        ascending=False
    )

    return score_df