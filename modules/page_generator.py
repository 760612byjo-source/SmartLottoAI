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

from modules.consensus_engine import (
    get_core_numbers
)

from modules.premium_generator import (
    generate_premium_numbers
)


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

    st.subheader("🎯 최종 번호 생성기")

    game_count = st.slider(
        "생성 게임수",
        min_value=1,
        max_value=20,
        value=10
    )

    if st.button("번호 생성"):

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

        core_numbers = get_core_numbers(
            results,
            top_n=6
        )

        premium_numbers = generate_premium_numbers(
            core_numbers,
            missing_numbers,
            count=5
        )

        st.success(
            f"{len(results)}게임 생성 완료"
        )

        for idx, item in enumerate(
            results,
            start=1
        ):

            st.write(
                f"{idx}위 ⭐ "
                f"({item['score']}점) : "
                + " ".join(
                    map(
                        str,
                        item["numbers"]
                    )
                )
            )

        st.subheader(
            "🔥 핵심번호 TOP6"
        )

        st.success(
            " / ".join(
                map(str, core_numbers)
            )
        )

        st.subheader(
            "👑 Premium 추천번호"
        )

        for idx, numbers in enumerate(
            premium_numbers,
            start=1
        ):

            st.write(
                f"{idx}번 : "
                + " ".join(
                    map(str, numbers)
                )
            )