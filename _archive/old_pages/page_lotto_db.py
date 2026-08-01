import streamlit as st
import pandas as pd
import plotly.express as px
import traceback

from modules.lotto_db import (
    get_lotto_history
)

from modules.exclude_engine import (
    calculate_excluded_numbers
)

from modules.include_engine import (
    calculate_included_numbers
)

def show_lotto_db_page():

    st.subheader("🎱 로또 데이터베이스")

    try:

        lotto = get_lotto_history()

        latest = lotto[
            lotto["회차"].notna()
        ].iloc[-1]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "총 회차",
                int(latest["회차"])
            )

        with col2:
            st.metric(
                "추첨일",
                str(latest["추첨일"])
            )

        st.markdown("---")

        st.subheader("최신 당첨번호")

        numbers = [
            latest["번호1"],
            latest["번호2"],
            latest["번호3"],
            latest["번호4"],
            latest["번호5"],
            latest["번호6"]
        ]

        st.success(
            "  ".join(
                [str(int(n)) for n in numbers]
            )
        )

        st.info(
            f"보너스 : {int(latest['보너스'])}"
        )

        st.markdown("---")

        st.subheader("최근 10회")

        st.dataframe(
            lotto.tail(10),
            use_container_width=True
        )

        # ==========================
        # 홀짝 분석
        # ==========================

        st.markdown("---")
        st.subheader("🎲 홀짝 분석")

        number_cols = [
            "번호1",
            "번호2",
            "번호3",
            "번호4",
            "번호5",
            "번호6"
        ]

        odd_even_results = []

        for _, row in lotto.iterrows():

            try:

                numbers = [
                    int(row[col])
                    for col in number_cols
                ]

                odd_count = sum(
                    n % 2 == 1
                    for n in numbers
                )

                even_count = 6 - odd_count

                pattern = f"{odd_count}:{even_count}"

                odd_even_results.append(pattern)

            except:
                pass

        # 패턴 집계
        pattern_series = pd.Series(
            odd_even_results
        ).value_counts()

        pattern_df = pd.DataFrame({
            "홀짝패턴": pattern_series.index,
            "출현횟수": pattern_series.values
        })

        pattern_df["비율(%)"] = round(
            pattern_df["출현횟수"]
            / pattern_df["출현횟수"].sum()
            * 100,
            2
        )

        st.dataframe(
            pattern_df,
            use_container_width=True
        )

        fig = px.bar(
            pattern_df,
            x="홀짝패턴",
            y="출현횟수",
            text="비율(%)",
            title="홀짝 패턴 분포"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
        best_pattern = pattern_df.iloc[0]

        st.success(
            f"""
        가장 많이 출현한 홀짝 패턴

        ✅ {best_pattern['홀짝패턴']}

        총 {best_pattern['출현횟수']}회

        비율 {best_pattern['비율(%)']}%
        """
        )

        st.markdown("---")

        st.subheader("📊 번호별 출현 횟수")

        # 번호 컬럼만 선택

        number_cols = [
            "번호1",
            "번호2",
            "번호3",
            "번호4",
            "번호5",
            "번호6"
        ]

        all_numbers = []

        for col in number_cols:

            all_numbers.extend(
                pd.to_numeric(
                    lotto[col],
                    errors="coerce"
                )
                .dropna()
                .astype(int)
                .tolist()
            )

        freq = (
            pd.Series(all_numbers)
            .value_counts()
            .sort_values(
                ascending=False
            )
        )

        # TOP10

        st.subheader("🔥 출현빈도 TOP10")

        top10 = freq.head(10)

        st.bar_chart(top10)

        # Bottom10

        st.subheader("❄ 출현빈도 Bottom10")

        bottom10 = (
            freq.sort_values()
            .head(10)
        )

        st.bar_chart(bottom10)

        # 전체표

        st.subheader("📋 전체 번호 빈도표")

        freq_df = pd.DataFrame({

            "번호": freq.index,
            "출현횟수": freq.values

        })

        st.dataframe(
            freq_df,
            use_container_width=True
        )

        # ==========================
        # 저고 분석
        # ==========================

        st.markdown("---")
        st.subheader("📊 저고 분석")

        low_high_results = []

        for _, row in lotto.iterrows():

            try:

                numbers = [
                    int(row[col])
                    for col in number_cols
                ]

                low_count = sum(
                    n <= 22
                    for n in numbers
                )

                high_count = 6 - low_count

                pattern = f"{low_count}:{high_count}"

                low_high_results.append(pattern)

            except:
                pass

        pattern_series = pd.Series(
            low_high_results
        ).value_counts()

        low_high_df = pd.DataFrame({
            "저고패턴": pattern_series.index,
            "출현횟수": pattern_series.values
        })

        low_high_df["비율(%)"] = round(
            low_high_df["출현횟수"]
            / low_high_df["출현횟수"].sum()
            * 100,
            2
        )

        st.dataframe(
            low_high_df,
            use_container_width=True
        )

        fig = px.bar(
            low_high_df,
            x="저고패턴",
            y="출현횟수",
            text="비율(%)",
            title="저고 패턴 분포"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==========================
        # 끝수 분석
        # ==========================

        st.markdown("---")
        st.subheader("🔢 끝수합 분석")

        end_sum_results = []

        for _, row in lotto.iterrows():

            try:

                numbers = [
                    int(row[col])
                    for col in number_cols
                ]

                end_sum = sum(
                    n % 10
                    for n in numbers
                )

                end_sum_results.append(end_sum)

            except:
                pass

        end_df = pd.DataFrame({
            "끝수합": end_sum_results
        })

        st.dataframe(
            end_df.describe(),
            use_container_width=True
        )

        bins = [
            0, 10, 15, 20, 25,
            30, 35, 40, 45, 50, 60
        ]

        labels = [
            "0~10",
            "11~15",
            "16~20",
            "21~25",
            "26~30",
            "31~35",
            "36~40",
            "41~45",
            "46~50",
            "51~60"
        ]

        end_df["구간"] = pd.cut(
            end_df["끝수합"],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

        end_pattern = (
            end_df["구간"]
            .value_counts()
            .sort_index()
        )

        end_pattern_df = pd.DataFrame({
            "끝수합구간": end_pattern.index.astype(str),
            "출현횟수": end_pattern.values
        })

        end_pattern_df["비율(%)"] = round(
            end_pattern_df["출현횟수"]
            /
            end_pattern_df["출현횟수"].sum()
            * 100,
            2
        )

        st.dataframe(
            end_pattern_df,
            use_container_width=True
        )

        fig = px.bar(
            end_pattern_df,
            x="끝수합구간",
            y="출현횟수",
            text="비율(%)",
            title="끝수합 구간 분포"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        best_end = end_pattern_df.sort_values(
            "출현횟수",
            ascending=False
        ).iloc[0]

        st.success(
            f"""
        가장 많이 출현한 끝수합 구간

        ✅ {best_end['끝수합구간']}

        총 {best_end['출현횟수']}회

        비율 {best_end['비율(%)']}%
        """
        )

        # ==========================
        # 소수 분석
        # ==========================

        st.markdown("---")
        st.subheader("🔷 소수 분석")

        PRIMES = [
            2, 3, 5, 7,
            11, 13, 17, 19,
            23, 29, 31, 37,
            41, 43
        ]

        prime_results = []

        for _, row in lotto.iterrows():

            try:

                numbers = [
                    int(row[col])
                    for col in number_cols
                ]

                prime_count = sum(
                    n in PRIMES
                    for n in numbers
                )

                prime_results.append(prime_count)

            except:
                pass

        prime_series = pd.Series(
            prime_results
        ).value_counts()

        prime_df = pd.DataFrame({
            "소수개수": prime_series.index,
            "출현횟수": prime_series.values
        })

        prime_df = prime_df.sort_values(
            "소수개수"
        )

        prime_df["비율(%)"] = round(
            prime_df["출현횟수"]
            /
            prime_df["출현횟수"].sum()
            * 100,
            2
        )

        st.dataframe(
            prime_df,
            use_container_width=True
        )

        fig = px.bar(
            prime_df,
            x="소수개수",
            y="출현횟수",
            text="비율(%)",
            title="소수 개수 분포"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        best_prime = prime_df.sort_values(
            "출현횟수",
            ascending=False
        ).iloc[0]

        st.success(
            f"""
        가장 많이 출현한 소수 개수

        ✅ {int(best_prime['소수개수'])}개

        총 {best_prime['출현횟수']}회

        비율 {best_prime['비율(%)']}%
        """
        )

        # ==========================
        # 최근출현수 분석
        # ==========================

        st.markdown("---")
        st.subheader("🔥 최근출현수 분석")

        recent_count = st.slider(
            "최근 회차 선택",
            min_value=10,
            max_value=100,
            value=20,
            step=10
        )

        recent_lotto = lotto.tail(recent_count)

        number_cols = [
            "번호1",
            "번호2",
            "번호3",
            "번호4",
            "번호5",
            "번호6"
        ]

        recent_numbers = []

        for col in number_cols:

            recent_numbers.extend(
                recent_lotto[col]
                .dropna()
                .astype(int)
                .tolist()
            )

        recent_freq = (
            pd.Series(recent_numbers)
            .value_counts()
        )

        recent_df = pd.DataFrame({
            "번호": recent_freq.index,
            "최근출현횟수": recent_freq.values
        })

        recent_df = recent_df.sort_values(
            "최근출현횟수",
            ascending=False
        )

        st.dataframe(
            recent_df,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🚀 강세수 TOP10")

        hot_numbers = recent_df.head(10)

        st.dataframe(
            hot_numbers,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("❄️ 약세수 TOP10")

        cold_numbers = recent_df.tail(10)

        st.dataframe(
            cold_numbers,
            use_container_width=True
        )

        fig = px.bar(
            hot_numbers,
            x="번호",
            y="최근출현횟수",
            text="최근출현횟수",
            title=f"최근 {recent_count}회 강세수 TOP10"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        best_number = hot_numbers.iloc[0]

        st.success(
            f"""
        최근 {recent_count}회 기준

        🏆 최강 강세수

        번호 : {int(best_number['번호'])}

        출현횟수 : {int(best_number['최근출현횟수'])}회
        """
        )

        # ==========================
        # 미출현수 분석
        # ==========================

        st.markdown("---")
        st.subheader("❄️ 미출현수 분석")

        missing_data = []

        for num in range(1, 46):

            miss_count = 0

            for i in range(len(lotto)-1, -1, -1):

                row = lotto.iloc[i]

                numbers = []

                try:

                    for col in number_cols:

                        numbers.append(
                            int(row[col])
                        )

                except:
                    continue

                if num in numbers:
                    break

                miss_count += 1

            missing_data.append(
                [num, miss_count]
            )

        missing_df = pd.DataFrame(
            missing_data,
            columns=[
                "번호",
                "미출현회수"
            ]
        )

        missing_df = missing_df.sort_values(
            "미출현회수",
            ascending=False
        )

        st.dataframe(
            missing_df,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🔥 장기 미출현수 TOP10")

        top_missing = missing_df.head(10)

        st.dataframe(
            top_missing,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("⚡ 최근 출현수 TOP10")

        recent_numbers = missing_df.sort_values(
            "미출현회수"
        ).head(10)

        st.dataframe(
            recent_numbers,
            use_container_width=True
        )

        fig = px.bar(
            top_missing,
            x="번호",
            y="미출현회수",
            text="미출현회수",
            title="장기 미출현수 TOP10"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        best_missing = top_missing.iloc[0]

        st.warning(
            f"""
        가장 오래 출현하지 않은 번호

        번호 : {int(best_missing['번호'])}

        미출현 : {int(best_missing['미출현회수'])}회
        """
        )

        # ==========================
        # 제외수 엔진
        # ==========================

        st.markdown("---")
        st.subheader("🚫 제외수 엔진")

        exclude_df = calculate_excluded_numbers(
            recent_df,
            missing_df
        )

        st.dataframe(
            exclude_df,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🚫 추천 제외수 TOP10")

        top_exclude = exclude_df.head(10)

        st.dataframe(
            top_exclude,
            use_container_width=True
        )

        fig = px.bar(
            top_exclude,
            x="번호",
            y="제외점수",
            text="제외점수",
            title="추천 제외수"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        exclude_numbers = (
            top_exclude["번호"]
            .astype(int)
            .tolist()
        )

        st.error(
            f"""
        추천 제외수

        {exclude_numbers}
        """
        )

        # ==========================
        # 포함수 엔진
        # ==========================

        st.markdown("---")
        st.subheader("✅ 포함수 엔진")

        include_df = calculate_included_numbers(
            recent_df,
            missing_df
        )

        st.dataframe(
            include_df,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("✅ 추천 포함수 TOP10")

        top_include = include_df.head(10)

        st.dataframe(
            top_include,
            use_container_width=True
        )

        fig = px.bar(
            top_include,
            x="번호",
            y="포함점수",
            text="포함점수",
            title="추천 포함수"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        include_numbers = (
            top_include["번호"]
            .astype(int)
            .tolist()
        )

        st.success(
            f"""
        추천 포함수

        {include_numbers}
        """
        )



    except Exception as e:
    
        st.error(traceback.format_exc())