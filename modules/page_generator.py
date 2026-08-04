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

            profile_summary = None
            rank100_summary = None

            candidate_count = 0
            profile3_count = 0

            if len(results) > 0:

                profile_summary = results[0].get(
                    "profile_summary"
                )

                rank100_summary = results[0].get(
                    "rank100_summary"
                )

                candidate_count = results[0].get(
                    "candidate_count",
                    0
                )

                profile3_count = results[0].get(
                    "profile3_count",
                    0
                )

            for item in results[:5]:

                save_recommendation(
                    item["numbers"]
                )

        st.subheader("🎯 LAI 추천")

        with st.container(border=True):

            rank_icons = [
                "🥇",
                "🥈",
                "🥉",
                "⭐",
                "⭐"
            ]

            for idx, item in enumerate(results[:5]):

                cols = st.columns(
                    [1.2,0.8,0.8,0.8,0.8,0.8,0.8]
                )

                cols[0].markdown(
                    f"<div style='font-size:28px'>{rank_icons[idx]}</div>",
                    unsafe_allow_html=True
                )

                for i, num in enumerate(
                    item["numbers"],
                    start=1
                ):

                    color = get_ball_color(num)

                    cols[i].markdown(
                        f"""
        <div style="
            width:34px; 
            height:34px;
            border-radius:50%;
            background:{color};
            color:white;
            font-weight:800;
            font-size:15px;
            text-align:center;
            line-height:34px;
            margin:auto;
            border:2px solid rgba(255,255,255,0.25);
        ">
            {num}
        </div>
        """,
                        unsafe_allow_html=True
                    )

                st.divider()

    st.markdown("### 🎯 생성번호 프로파일")

    summary_df = pd.DataFrame([
        {
            "구분": "현재",
            "Profile3+": profile3_count,
            "후보수": candidate_count,
        },
        {
            "구분": "기준",
            "Profile3+": "50+",
            "후보수": "충분",
        }
    ])

    st.dataframe(
        summary_df,
        hide_index=True,
        use_container_width=True
    )

    if profile_summary:

        profile_df = pd.DataFrame(
            {
                "Profile": list(profile_summary.keys()),
                "Count": list(profile_summary.values())
            }
        )

        st.dataframe(
            profile_df,
            hide_index=True,
            use_container_width=True
        )