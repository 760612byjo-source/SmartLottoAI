import streamlit as st
import pandas as pd
import plotly.express as px

from modules.lotto_db import (
    get_lotto_history
)

from modules.backtest_engine import (
    run_backtest
)

from modules.adaptive_trainer import (
    train_all_weights
)

def show_backtest_page():

    st.title("📊 백테스트 엔진")

    lotto = get_lotto_history()

    st.markdown("---")

    start_idx = st.slider(
        "시작 인덱스",
        min_value=100,
        max_value=len(lotto)-1,
        value=300
    )

    game_count = st.slider(
        "생성 게임 수",
        min_value=1,
        max_value=20,
        value=10
    )

    use_adaptive = st.checkbox(
        "Adaptive 적용",
        value=True
    )

    st.info(
        f"""
시작위치 : {start_idx}

예측게임수 : {game_count}
"""
    )

    if st.button("🚀 백테스트 실행"):

        with st.spinner(
            "백테스트 실행 중..."
        ):

            result_df = run_backtest(
                lotto,
                start_idx,
                game_count,
                use_adaptive=use_adaptive
            )
        
        adaptive_weights = train_all_weights(
            result_df
        )

        st.markdown("---")

        st.subheader(
            "🧠 Adaptive 학습 결과"
        )

        st.json(
            adaptive_weights
        )

        st.success("백테스트 완료")

        st.subheader("📋 백테스트 결과")

        st.dataframe(
            result_df,
            use_container_width=True
        )

        # ==========================
        # 성능 요약
        # ==========================

        avg_hit = round(
            result_df["적중수"].mean(),
            2
        )

        max_hit = (
            result_df["적중수"]
            .max()
        )

        hit3 = len(
            result_df[
                result_df["적중수"] >= 3
            ]
        )

        hit3_rate = round(
            hit3
            /
            len(result_df)
            * 100,
            2
        )

        hit4 = len(
            result_df[
                result_df["적중수"] >= 4
            ]
        )

        hit4_rate = round(
            hit4
            /
            len(result_df)
            * 100,
            2
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "평균 적중수",
                avg_hit
            )

        with col2:

            st.metric(
                "최고 적중수",
                max_hit
            )

        with col3:

            st.metric(
                "3개 이상 적중률",
                f"{hit3_rate}%"
            )

        with col4:

            st.metric(
                "4개 이상 적중률",
                f"{hit4_rate}%"
            )

        # ==========================
        # 적중 분포
        # ==========================

        st.markdown("---")
        st.subheader("🎯 적중 분포")

        hit_counts = (
            result_df["적중수"]
            .value_counts()
            .sort_index()
        )

        hit_df = hit_counts.reset_index()

        hit_df.columns = [
            "적중수",
            "횟수"
        ]

        st.dataframe(
            hit_df,
            use_container_width=True
        )

        fig = px.bar(
            hit_df,
            x="적중수",
            y="횟수",
            text="횟수",
            title="적중수 분포"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "📈 회차별 적중 추세"
        )

        chart_df = (
            result_df[
                ["회차", "적중수"]
            ]
            .set_index("회차")
        )

        st.line_chart(
            chart_df
        )

        st.markdown("---")

        best_row = result_df.loc[
            result_df["적중수"]
            .idxmax()
        ]

        st.success(
            f"""
최고 적중 회차

회차 : {best_row['회차']}

적중수 : {best_row['적중수']}개
"""
        )

    st.markdown("---")

    if st.button(
        "📊 Adaptive 성능 비교"
    ):

        with st.spinner(
            "Adaptive 비교 중..."
        ):

            result_off = run_backtest(
                lotto,
                start_idx,
                game_count,
                use_adaptive=False
            )

            result_on = run_backtest(
                lotto,
                start_idx,
                game_count,
                use_adaptive=True
            )

        compare_df = pd.DataFrame({

            "구분": [
                "Adaptive OFF",
                "Adaptive ON"
            ],

            "평균적중수": [

                round(
                    result_off["적중수"].mean(),
                    2
                ),

                round(
                    result_on["적중수"].mean(),
                    2
                )

            ],

            "최고적중수": [

                result_off["적중수"].max(),

                result_on["적중수"].max()

            ],

            "3개이상적중률": [

                round(
                    (
                        result_off["적중수"] >= 3
                    ).mean() * 100,
                    2
                ),

                round(
                    (
                        result_on["적중수"] >= 3
                    ).mean() * 100,
                    2
                )

            ],

            "4개이상적중률": [

                round(
                    (
                        result_off["적중수"] >= 4
                    ).mean() * 100,
                    2
                ),

                round(
                    (
                        result_on["적중수"] >= 4
                    ).mean() * 100,
                    2
                )

            ]

        })       

        st.subheader(
            "📊 Adaptive 비교 결과"
        )

        st.dataframe(
            compare_df,
            use_container_width=True
        )

        off_avg = (
            result_off["적중수"]
            .mean()
        )

        on_avg = (
            result_on["적중수"]
            .mean()
        )

        if on_avg > off_avg:

            st.success(
                f"Adaptive 적용 성능 향상 (+{round(on_avg-off_avg,2)})"
            )

        elif on_avg < off_avg:

            st.warning(
                f"Adaptive 적용 성능 하락 ({round(on_avg-off_avg,2)})"
            )

        else:

            st.info(
                "성능 차이 없음"
            )            

