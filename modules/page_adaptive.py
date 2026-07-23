import streamlit as st
import pandas as pd
import os

from datetime import datetime

from modules.adaptive_engine import (
    load_adaptive_weights,
    initialize_adaptive_weights
)

from modules.lotto_db import (
    get_lotto_history
)


def show_adaptive_page():

    st.title(
        "🧠 Adaptive Engine"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Adaptive 재학습"
        ):

            lotto = get_lotto_history()

            initialize_adaptive_weights(
                lotto
            )

            st.success(
                "Adaptive 재학습 완료"
            )

    with col2:

        if st.button(
            "📂 가중치 다시 불러오기"
        ):

            st.success(
                "가중치 새로고침 완료"
            )
    
    if os.path.exists(
        "data/adaptive_weights.json"
    ):

        modified_time = datetime.fromtimestamp(
            os.path.getmtime(
                "data/adaptive_weights.json"
            )
        )

        st.info(
            f"""
    최근 학습 시간

    {modified_time}
    """
        )

    weights = load_adaptive_weights()

    if weights is None:

        st.warning(
            "Adaptive 가중치 파일이 없습니다."
        )

        return

    st.subheader(
        "홀짝 가중치"
    )

    odd_df = pd.DataFrame(
        list(
            weights["odd_even"].items()
        ),
        columns=[
            "패턴",
            "가중치"
        ]
    )

    st.dataframe(
        odd_df,
        use_container_width=True
    )

    st.subheader(
        "저고 가중치"
    )

    low_df = pd.DataFrame(
        list(
            weights["low_high"].items()
        ),
        columns=[
            "패턴",
            "가중치"
        ]
    )

    st.dataframe(
        low_df,
        use_container_width=True
    )

    st.subheader(
        "소수 가중치"
    )

    prime_df = pd.DataFrame(
        list(
            weights["prime"].items()
        ),
        columns=[
            "소수개수",
            "가중치"
        ]
    )

    st.dataframe(
        prime_df,
        use_container_width=True
    )

    st.subheader(
        "끝수합 가중치"
    )

    end_df = pd.DataFrame(
        list(
            weights["endsum"].items()
        ),
        columns=[
            "끝수합구간",
            "가중치"
        ]
    )

    st.dataframe(
        end_df,
        use_container_width=True
    )
