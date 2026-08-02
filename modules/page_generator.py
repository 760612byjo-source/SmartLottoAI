import streamlit as st

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

        st.subheader("🎯 LAI 추천")

with st.container(border=True):

    rank_icons = [
        "🥇",
        "🥈",
        "🥉",
        "⭐",
        "⭐"
    ]

    for idx, item in enumerate(
        results[:5]
    ):

        balls_html = ""

        for num in item["numbers"]:

            color = get_ball_color(num)

            balls_html += f"""
            <span style="
                display:inline-flex;
                width:48px;
                height:48px;
                border-radius:50%;
                background:{color};
                color:white;
                font-weight:800;
                font-size:22px;
                align-items:center;
                justify-content:center;
                margin-right:8px;
                margin-bottom:8px;
            ">
                {num}
            </span>
            """

        st.markdown(
            f"""
            <div style="
                padding:15px 0;
            ">

                <div style="
                    font-size:30px;
                    margin-bottom:12px;
                ">
                    {rank_icons[idx]}
                </div>

                <div>
                    {balls_html}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if idx < 4:
            st.divider()