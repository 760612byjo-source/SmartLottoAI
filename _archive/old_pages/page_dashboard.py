import streamlit as st
import pandas as pd
import plotly.express as px

from modules.lotto_db import (
    get_lotto_history
)

from modules.lotto_analysis import (
    get_recent_df,
    get_missing_df
)


def show_dashboard_page():

    st.title("📊 SmartLottoAI 통계대시보드")

    lotto = get_lotto_history()

    recent_df = get_recent_df()

    missing_df = get_missing_df()

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

    st.subheader("🔥 출현빈도 TOP10")

    top10 = freq.head(10)

    st.bar_chart(top10)

    st.subheader("❄ 출현빈도 Bottom10")

    bottom10 = (
        freq.sort_values()
        .head(10)
    )

    st.bar_chart(bottom10)

    st.subheader("📋 전체 번호 빈도표")

    freq_df = pd.DataFrame({
        "번호": freq.index,
        "출현횟수": freq.values
    })

    st.dataframe(
        freq_df,
        use_container_width=True
    )

    odd_count = sum(
        n % 2 == 1
        for n in all_numbers
    )

    even_count = sum(
        n % 2 == 0
        for n in all_numbers
    )

    odd_even_df = pd.DataFrame({

        "구분": ["홀수", "짝수"],
        "개수": [odd_count, even_count]

    })

    fig = px.pie(
        odd_even_df,
        names="구분",
        values="개수",
        title="홀짝 비율"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    low_count = sum(
        n <= 22
        for n in all_numbers
    )

    high_count = sum(
        n >= 23
        for n in all_numbers
    )

    low_high_df = pd.DataFrame({

        "구분": ["저번호", "고번호"],
        "개수": [low_count, high_count]

    })

    fig = px.pie(
        low_high_df,
        names="구분",
        values="개수",
        title="저고 비율"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    sections = {
        "1~10": 0,
        "11~20": 0,
        "21~30": 0,
        "31~40": 0,
        "41~45": 0
    }

    for n in all_numbers:

        if n <= 10:
            sections["1~10"] += 1

        elif n <= 20:
            sections["11~20"] += 1

        elif n <= 30:
            sections["21~30"] += 1

        elif n <= 40:
            sections["31~40"] += 1

        else:
            sections["41~45"] += 1

    section_df = pd.DataFrame({
        "구간": sections.keys(),
        "출현수": sections.values()
    })

    fig = px.bar(
        section_df,
        x="구간",
        y="출현수",
        title="번호구간 분포"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🔥 강세수 TOP15")

    st.dataframe(
        recent_df.head(15),
        use_container_width=True
    )

    st.subheader("❄ 장기미출현수 TOP15")

    st.dataframe(
        missing_df.head(15),
        use_container_width=True
    )