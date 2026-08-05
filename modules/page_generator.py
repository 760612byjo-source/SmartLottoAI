import streamlit as st
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

from modules.update_manager import (
    get_update_status
)

from datetime import datetime

from modules.recommend_store import (
    save_recommendation
)

def get_ball_color(number):

    if number <= 10:
        return "#fbc400"    # 노랑

    elif number <= 20:
        return "#69c8f2"    # 파랑

    elif number <= 30:
        return "#ff7272"    # 빨강

    elif number <= 40:
        return "#aaaaaa"    # 회색(검정대신)

    else:
        return "#b0d840"    # 초록


def show_generator_page():

    profile_summary = None
    rank100_summary = None

    candidate_count = 0
    profile3_count = 0

    results = []

    recent_df = get_recent_df()

    missing_df = get_missing_df()

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

    exclude_df = calculate_excluded_numbers(
        recent_df,
        missing_df
    )

    include_df = calculate_included_numbers(
        recent_df,
        missing_df
    )

    st.subheader("🎯 추천번호 생성")

    status = get_update_status()

    st.caption(
        f"최신 데이터 반영 : {status['db_draw']}회"
    )

    st.markdown("")

    game_count = 5

    if st.button("🎯 추천번호 생성"):

        with st.spinner(
            "🎱 LAI 분석 엔진 실행 중..."
        ):

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

            debug_info = None

            for item in results:

                if item.get("_debug"):

                    debug_info = item
                    break

            if debug_info:

                st.subheader("📊 Profile 분포")

                st.dataframe(
                    pd.DataFrame(
                        list(
                            debug_info["profile_dist"].items()
                        ),
                        columns=[
                            "Profile",
                            "Count"
                        ]
                    )
                )

                st.write(
                    f"candidate_df : "
                    f"{debug_info['candidate_count']}"
                )

            results = generate_numbers(
                exclude_numbers,
                include_numbers,
                hot_numbers,
                missing_numbers,
                game_count
            )

            for item in results[:5]:

                save_recommendation(
                    item["numbers"]
                )

        st.subheader("🎯 LAI 추천")

        fitness_map = {
            45: "B+",
            50: "B",
            55: "A+",
            60: "A",
            65: "C+",
            70: "C"
        }

        result_table = []

        for idx, item in enumerate(results[:10]):

            result_table.append(
                {
                    "번호": idx + 1,
                    "추천번호": " · ".join(
                        map(str, item["numbers"])
                    ),
                    "Profile": item.get(
                        "profile_score",
                        "-"
                    ),
                    "적합도": fitness_map.get(
                        item.get("rank100", 0),
                        "-"
                    )
                }
            )

        st.dataframe(
            pd.DataFrame(result_table),
            hide_index=True,
            use_container_width=True
        )