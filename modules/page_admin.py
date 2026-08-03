# modules/page_admin.py

import streamlit as st
import pandas as pd

from modules.pair_builder import (
    save_pair_cache
)

from modules.triple_builder import (
    save_triple_cache
)

from modules.update_manager import (
    run_full_update,
    get_update_status,
    get_cache_status,
    get_missing_draws,
    load_update_status_log
)

from modules.window_pattern_engine import (
    build_window_patterns,
    show_window_patterns,
    calculate_window_pattern_score
)

from modules.score_analyzer import (
    analyze_winner_scores
)

from modules.lotto_db import (
    get_lotto_history
)

from modules.recommend_store import (
    load_recommendations,
    delete_all_recommendations,
    delete_recommendation
)

from modules.pair_engine import (
    load_pair_cache,
    calculate_pair_score
)

from modules.triple_engine import (
    load_triple_cache,
    calculate_triple_score
)

from modules.score_engine import (
    calculate_score
)

from modules.number_generator import (
    calculate_score_detail
)

def show_admin_page():

    if "logs" not in st.session_state:
        st.session_state.logs = []

    st.title("⚙️ 시스템 관리")

    st.markdown("---")

    status = get_update_status()
    cache_info = get_cache_status()

    missing_draws = get_missing_draws()
    update_range = ""

    if missing_draws:

        update_range = (
            f"{missing_draws[0]}회 ~ "
            f"{missing_draws[-1]}회"
        )


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "DB 회차",
            f"{status['db_draw']:,}"
        )

    with col2:
        st.metric(
            "최신 회차",
            f"{status['latest_draw']:,}"
        )

    with col3:
        st.metric(
            "누락 회차",
            f"{len(missing_draws):,}"
        )

    with col4:
        st.metric(
            "Pair Cache",
            f"{cache_info['pair_count']:,}"
        )

    with col5:
        st.metric(
            "Triple Cache",
            f"{cache_info['triple_count']:,}"
        )

    if status["need_update"]:

        st.warning(
            "⚠️ 업데이트 필요"
        )

    if missing_draws:

        st.info(
            f"📥 업데이트 대상 : "
            f"{update_range} "
            f"({len(missing_draws):,}회)"
        )

    else:

        st.success(
            "✅ 최신 상태"
        )

    st.info(
        """
    전체 업데이트 실행

    1. 누락 회차 자동 보충
    2. Pair Cache 재생성
    3. Triple Cache 재생성
    4. 상태 로그 저장
    """
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🚀 전체 업데이트",
            use_container_width=True
        ):

            with st.spinner(
                "전체 업데이트 진행 중..."
            ):

                st.session_state.logs = run_full_update()

            st.success(
                "✅ 전체 업데이트 완료"
            )
        
        if st.session_state.logs:

            with st.expander(
                "업데이트 로그"
            ):

                for log in st.session_state.logs:
                    st.write(log)

    with col2:

        if st.button(
            "⚡ Cache 재생성",
            use_container_width=True
        ):

            with st.spinner("Cache 재생성 중..."):

                pair_count, triple_count = rebuild_cache_only()

            st.success(
                f"✅ Cache 재생성 완료\n"
                f"   Pair Cache: {pair_count:,}개\n"
                f"   Triple Cache: {triple_count:,}개"
            )

        if st.button(
            "📊 Multi-Window 분석",
            use_container_width=True
        ):

            lotto_df = get_lotto_history()

            patterns = build_window_patterns(
                lotto_df
            )

            show_window_patterns(
                patterns
            )

        if st.button(
            "🏆 당첨번호 점수 분석",
            use_container_width=True
        ):

            lotto_df = get_lotto_history()

            result_df, summary = (
                analyze_winner_scores(
                    lotto_df
                )
            )

            st.write(
                f"평균 점수 : {summary['평균']}"
            )

            st.write(
                f"최소 점수 : {summary['최소']}"
            )

            st.write(
                f"최대 점수 : {summary['최대']}"
            )

            st.write(
                f"중앙값 : {summary['중앙값']}"
            )

            st.write(
                f"Base 평균 : "
                f"{summary['Base평균']}"
            )

            st.write(
                f"Pair 평균 : "
                f"{summary['Pair평균']}"
            )

            st.write(
                f"Triple 평균 : "
                f"{summary['Triple평균']}"
            )

            st.write(
                f"Window 평균 : "
                f"{summary['Window평균']}"
            )

            st.write(
                f"Base 추천범위 : "
                f"{summary['Base_10']} ~ "
                f"{summary['Base_90']}"
            )

            st.write(
                f"Pair 추천범위 : "
                f"{summary['Pair_10']} ~ "
                f"{summary['Pair_90']}"
            )

            st.write(
                f"Triple 추천범위 : "
                f"{summary['Triple_10']} ~ "
                f"{summary['Triple_90']}"
            )

            st.write(
                f"Window 추천범위 : "
                f"{summary['Window_10']} ~ "
                f"{summary['Window_90']}"
            )

            st.write(
                f"상위80% 구간 : "
                f"{summary['상위80%_하한']} ~ "
                f"{summary['상위80%_상한']}"
            )

            st.write(
                f"LAI 평균 : "
                f"{summary['LAI평균']}"
            )

            st.write(
                f"LAI 추천범위 : "
                f"{summary['LAI_10']} ~ "
                f"{summary['LAI_90']}"
            )

            st.write(
                f"LAI 25% : {summary['LAI_25']}"
            )

            st.write(
                f"LAI 50% : {summary['LAI_50']}"
            )

            st.write(
                f"LAI 75% : {summary['LAI_75']}"
            )

            st.write(
                f"LAI 최소 : "
                f"{summary['LAI최소']}"
            )

            st.write(
                f"LAI 최대 : "
                f"{summary['LAI최대']}"
            )

            st.write(
                f"LAI75+ Pair 평균 : "
                f"{summary['LAI75_Pair']}"
            )

            st.write(
                f"LAI75+ Triple 평균 : "
                f"{summary['LAI75_Triple']}"
            )

            st.write(
                f"LAI75+ Base 평균 : "
                f"{summary['LAI75_Base']}"
            )

            st.write(
                f"LAI75+ Window 평균 : "
                f"{summary['LAI75_Window']}"
            )

            st.subheader(
                "🏆 상위 20개 점수"
            )

            top20_df = (
                result_df
                .sort_values(
                    "total",
                    ascending=False
                )
                .head(20)
            )

            st.dataframe(
                top20_df,
                use_container_width=True
            )

            st.subheader(
                "🎯 LAI 상위 20개"
            )

            top20_lai_df = (
                result_df
                .sort_values(
                    "lai_score",
                    ascending=False
                )
                .head(20)
            )

            st.dataframe(
                top20_lai_df,
                use_container_width=True
            )

            st.subheader(
                "📉 하위 20개 점수"
            )

            bottom20_df = (
                result_df
                .sort_values(
                    "total",
                    ascending=True
                )
                .head(20)
            )

            st.dataframe(
                bottom20_df,
                use_container_width=True
            )

            st.subheader(
                "📊 점수 분포 분석"
            )

            score_cols = [
                "total",
                "base",
                "pair",
                "triple",
                "window"
            ]

            for col in score_cols:

                st.markdown(
                    f"### {col}"
                )
        
                dist_df = (
                    pd.cut(
                        result_df[col],
                        bins=20
                    )
                    .value_counts()
                    .sort_index()
                    .reset_index()
                )

                dist_df.columns = [
                    "구간",
                    "개수"
                ]

                dist_df["구간"] = (
                    dist_df["구간"]
                    .astype(str)
                )

                st.dataframe(
                    dist_df,
                    use_container_width=True
                )

                st.bar_chart(
                    dist_df.set_index(
                        "구간"
                    )
                )

        if st.button(
            "🎲 생성번호 점수 분석",
            use_container_width=True
        ):

            lotto_df = get_lotto_history()

            pair_cache = load_pair_cache()

            triple_cache = load_triple_cache()

            window_patterns = (
                build_window_patterns(
                    lotto_df
                )
            )

            generated = generate_numbers(
                exclude_numbers=[],
                include_numbers=[],
                hot_numbers=[],
                missing_numbers=[],
                count=1000  
            )

            from modules.consensus_engine import (
                get_core_numbers
            )

            from modules.premium_generator import (
                generate_premium_numbers
            )

            st.write(
                f"생성 개수 : {len(generated)}"
            )

            if len(generated) == 0:

                st.error(
                    "생성된 번호가 없습니다."
                )

                return

            results = []

            for item in generated:

                numbers = item["numbers"]

                base_score = (
                    calculate_score(
                        numbers,
                        [],
                        [],
                        []
                    )
                )

                pair_score = (
                    calculate_pair_score(
                        numbers,
                        pair_cache
                    )
                )

                triple_score = (
                    calculate_triple_score(
                        numbers,
                        triple_cache
                    )
                )

                window_score = (
                    calculate_window_pattern_score(
                        numbers,
                        window_patterns
                    )
                )

                detail = (
                    calculate_score_detail(
                        base_score,
                        pair_score,
                        triple_score,
                        0,
                        window_score
                    )
                )

                results.append({

                    "numbers":
                    ",".join(
                        map(
                            str,
                            item["numbers"]
                        )
                    ),

                    "base":
                    detail["base"],

                    "pair":
                    detail["pair"],

                    "triple":
                    detail["triple"],

                    "window":
                    detail["window"],

                    "total":
                    detail["total"],

                    "raw_score":
                    item["score"],

                    "lai_score":
                    item["score"]
                })

            core_numbers = get_core_numbers(
                generated,
                top_n=6
            )

            premium_numbers = generate_premium_numbers(
                core_numbers,
                [],
                count=5
            )


            result_df = pd.DataFrame(
                results
            )

            result_df["distance"] = (
                abs(result_df["base"] - 51.41)
                +
                abs(result_df["pair"] - 294.33)
                +
                abs(result_df["triple"] - 54.09)
                +
                abs(result_df["window"] - 13.70)
            )

            # =========================
            # 당첨번호 프로파일 기준
            # =========================

            PROFILE_BASE_MIN = 49
            PROFILE_BASE_MAX = 61

            PROFILE_PAIR_MIN = 268
            PROFILE_PAIR_MAX = 317.9

            PROFILE_TRIPLE_MIN = 45
            PROFILE_TRIPLE_MAX = 64

            PROFILE_WINDOW_MIN = 10
            PROFILE_WINDOW_MAX = 17

            profile_df = result_df[

                (result_df["base"] >= PROFILE_BASE_MIN)
                &
                (result_df["base"] <= PROFILE_BASE_MAX)

                &

                (result_df["pair"] >= PROFILE_PAIR_MIN)
                &
                (result_df["pair"] <= PROFILE_PAIR_MAX)

                &

                (result_df["triple"] >= PROFILE_TRIPLE_MIN)
                &
                (result_df["triple"] <= PROFILE_TRIPLE_MAX)

                &

                (result_df["window"] >= PROFILE_WINDOW_MIN)
                &
                (result_df["window"] <= PROFILE_WINDOW_MAX)

            ]


            st.write(
                f"프로파일 통과 : "
                f"{len(profile_df):,} / "
                f"{len(result_df):,}"
            )

            st.write(
                f"통과율 : "
                f"{len(profile_df)/len(result_df)*100:.2f}%"
            )

            st.subheader(
                "🎲 생성번호 프로파일"
            )

            st.write(
                f"Base 평균 : "
                f"{result_df['base'].mean():.2f}"
            )

            st.write(
                f"Pair 평균 : "
                f"{result_df['pair'].mean():.2f}"
            )

            st.write(
                f"Triple 평균 : "
                f"{result_df['triple'].mean():.2f}"
            )

            st.write(
                f"Window 평균 : "
                f"{result_df['window'].mean():.2f}"
            )

            triple_pass = len(

                result_df[
                    result_df["triple"] >= 48
                ]

            )

            st.write(
                f"Triple 48+ : "
                f"{triple_pass:,} / "
                f"{len(result_df):,}"
            )

            st.write(
                f"Triple 통과율 : "
                f"{triple_pass / len(result_df) * 100:.2f}%"
            )

            score_cols = [
                "base",
                "pair",
                "triple",
                "window",
                "total"
            ]

            st.write(
                f"Triple 최대 : "
                f"{result_df['triple'].max():.2f}"
            )

            st.write(
                f"Triple 상위10 평균 : "
                f"{result_df['triple'].nlargest(10).mean():.2f}"
            )

            st.write(
                f"Triple 상위50 평균 : "
                f"{result_df['triple'].nlargest(50).mean():.2f}"
            )

            top50 = result_df.nlargest(
                50,
                "lai_score"
            )

            distance_top50 = result_df.nsmallest(
                50,
                "distance"
            )

            final_recommendation = distance_top50[
                (distance_top50["distance"] <= 8)
                &
                (distance_top50["pair"].between(290, 300))
                &
                (distance_top50["triple"] >= 53)
            ].copy()

            st.write(
                f"Distance 최소 : "
                f"{distance_top50['distance'].min():.2f}"
            )

            st.write(
                f"Distance 평균 : "
                f"{distance_top50['distance'].mean():.2f}"
            )

            st.write(
                f"Distance 최대 : "
                f"{distance_top50['distance'].max():.2f}"
            )
            st.write(
                f"Distance TOP50 LAI 평균 : "
                f"{distance_top50['lai_score'].mean():.2f}"
            )

            st.subheader(
                "TOP50 상세 목록"
            )

            st.dataframe(
                top50,
                use_container_width=True
            )

            st.subheader("🏆 최종 추천번호")

            st.dataframe(
                final_recommendation[
                    [
                        "numbers",
                        "distance",
                        "lai_score",
                        "pair",
                        "triple"
                    ]
                ],
                use_container_width=True
            )

            freq_df = get_number_frequency(
                final_recommendation
            )

            st.subheader(
                "📊 Elite 번호 출현 빈도"
            )

            st.dataframe(
                freq_df,
                use_container_width=True
            )

            st.subheader(
                "🔥 Elite 핵심번호 TOP10"
            )

            st.dataframe(
                freq_df.head(10),
                use_container_width=True
            )

            st.write(
                f"TOP50 Base 차이 : "
                f"{top50['base'].mean() - 51.41:.2f}"
            )

            st.write(
                f"TOP50 Pair 차이 : "
                f"{top50['pair'].mean() - 294.33:.2f}"
            )

            st.write(
                f"TOP50 Triple 차이 : "
                f"{top50['triple'].mean() - 54.09:.2f}"
            )

            st.write(
                f"TOP50 Window 차이 : "
                f"{top50['window'].mean() - 13.70:.2f}"
            )

            st.write(
                f"TOP50 Pair 10% : "
                f"{top50['pair'].quantile(0.10):.2f}"
            )

            st.write(
                f"TOP50 Pair 90% : "
                f"{top50['pair'].quantile(0.90):.2f}"
            )

            st.write(
                f"TOP50 Base 10% : "
                f"{top50['base'].quantile(0.10):.2f}"
            )

            st.write(
                f"TOP50 Base 90% : "
                f"{top50['base'].quantile(0.90):.2f}"
            )

            st.write(
                f"TOP50 Triple 10% : "
                f"{top50['triple'].quantile(0.10):.2f}"
            )

            st.write(
                f"TOP50 Triple 90% : "
                f"{top50['triple'].quantile(0.90):.2f}"
            )

            for col in score_cols:

                st.markdown(
                    f"### {col}"
                )

                dist_df = (
                    pd.cut(
                        result_df[col],
                        bins=20
                    )
                    .value_counts()
                    .sort_index()
                    .reset_index()
                )

                dist_df.columns = [
                    "구간",
                    "개수"
                ]

                dist_df["구간"] = (
                    dist_df["구간"]
                    .astype(str)
                )

                st.dataframe(
                    dist_df,
                    use_container_width=True
                )

                st.bar_chart(
                    dist_df.set_index(
                        "구간"
                    )
                )

            st.write(
                f"평균 점수 : {result_df['total'].mean():.2f}"
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

        st.markdown("---")

        st.subheader("🔍 단일 번호 분석")

        numbers_text = st.text_input(
            "번호 입력",
            placeholder="예: 6,7,11,15,39,43"
        )

        if st.button("🔍 분석 실행"):

            try:

                numbers = sorted(
                    [
                        int(x.strip())
                        for x in numbers_text.split(",")
                    ]
                )

                if len(numbers) != 6:

                    st.error(
                        "번호는 반드시 6개 입력해야 합니다."
                    )

                elif len(set(numbers)) != 6:

                    st.error(
                        "중복 번호가 있습니다."
                    )

                else:

                    total = sum(numbers)

                    odd_count = sum(
                        n % 2
                        for n in numbers
                    )

                    even_count = (
                        6 - odd_count
                    )

                    low_count = len(
                        [
                            n for n in numbers
                            if n <= 22
                        ]
                    )

                    high_count = (
                        6 - low_count
                    )

                    consecutive = []

                    for i in range(5):

                        if (
                            numbers[i + 1]
                            ==
                            numbers[i] + 1
                        ):

                            consecutive.append(
                                f"{numbers[i]}-{numbers[i+1]}"
                            )

                    st.markdown("### 📊 분석 결과")

                    c1, c2 = st.columns(2)

                    with c1:

                        st.metric(
                            "번호합",
                            total
                        )

                        st.metric(
                            "홀짝",
                            f"{odd_count}:{even_count}"
                        )

                    with c2:

                        st.metric(
                            "고저",
                            f"{low_count}:{high_count}"
                        )

                        st.metric(
                            "연번",
                            len(consecutive)
                        )

                    st.write(
                        f"번호: {numbers}"
                    )

                    st.write(
                        "연번 목록:",
                        ", ".join(consecutive)
                        if consecutive
                        else "없음"
                    )

                    lotto_df = get_lotto_history()

                    pair_cache = load_pair_cache()

                    triple_cache = load_triple_cache()

                    window_patterns = (
                        build_window_patterns(
                            lotto_df
                        )
                    )

                    base_score = calculate_score(
                        numbers,
                        [],
                        [],
                        []
                    )

                    pair_score = calculate_pair_score(
                        numbers,
                        pair_cache
                    )

                    triple_score = calculate_triple_score(
                        numbers,
                        triple_cache
                    )

                    window_score = (
                        calculate_window_pattern_score(
                            numbers,
                            window_patterns
                        )
                    )

                    detail = (
                        calculate_score_detail(
                            base_score,
                            pair_score,
                            triple_score,
                            0,
                            window_score
                        )
                    )

                    WINNER_AVG_BASE = 51.41
                    WINNER_AVG_PAIR = 294.33
                    WINNER_AVG_TRIPLE = 54.09
                    WINNER_AVG_WINDOW = 13.70

                    base_diff = (
                        detail["base"]
                        - WINNER_AVG_BASE
                    )

                    pair_diff = (
                        detail["pair"]
                        - WINNER_AVG_PAIR
                    )

                    triple_diff = (
                        detail["triple"]
                        - WINNER_AVG_TRIPLE
                    )

                    window_diff = (
                        detail["window"]
                        - WINNER_AVG_WINDOW
                    )

                    total_score = round(

                        (
                            detail["base"]
                            + detail["pair"]
                            + detail["triple"]
                            + detail["window"]
                        ) / 4,

                        2
                    )

                    st.markdown(
                        "### 📈 최근 당첨평균 대비"
                    )

                    compare_df = pd.DataFrame({

                        "항목": [
                            "Base",
                            "Pair",
                            "Triple",
                            "Window"
                        ],

                        "현재값": [

                            round(detail["base"], 2),

                            round(detail["pair"], 2),

                            round(detail["triple"], 2),

                            round(detail["window"], 2)
                        ],

                        "당첨평균": [

                            WINNER_AVG_BASE,
                            WINNER_AVG_PAIR,
                            WINNER_AVG_TRIPLE,
                            WINNER_AVG_WINDOW
                        ],

                        "차이": [

                            round(base_diff, 2),

                            round(pair_diff, 2),

                            round(triple_diff, 2),

                            round(window_diff, 2)
                        ]

                    })

                    st.dataframe(
                        compare_df,
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    f"에러 발생 : {e}"
                )

    if missing_draws:

        preview = ", ".join(
            map(
                str,
                missing_draws[:10]
            )
        )

        st.caption(
            f"누락 회차 예시 : {preview} ..."
            f"(총 {len(missing_draws):,}회)"
        )

    status_log = load_update_status_log()

    if status_log:

        st.subheader("📋 마지막 업데이트")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "최종 업데이트",
                status_log["last_update"]
            )

        with c2:
            st.metric(
                "최신회차",
                status_log["latest_draw"]
            )

        with c3:
            st.metric(
                "성공",
                status_log["success_count"]
            )

        with c4:
            st.metric(
                "실패",
                status_log["failed_count"]
            )

        st.markdown("---")

        st.subheader(
            "📁 추천번호 보관함"
        )

        history_df = load_recommendations()

        search_text = st.text_input(
            "🔍 추천번호 검색",
            placeholder="번호 입력 (예: 42)"
        )

        if search_text:

            history_df = history_df[

                history_df["numbers"]
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )

            ]

        st.info(
            f"검색 결과 : {len(history_df):,}건"
        )

        if not history_df.empty:

            history_df = history_df.sort_values(
                "created_at",
                ascending=False
            )

        for idx, row in history_df.iterrows():

            col1, col2, col3 = st.columns(
                [2, 4, 1]
            )

            with col1:

                st.write(
                    row["created_at"]
                )

            with col2:

                st.write(
                    row["numbers"]
                )

            with col3:

                if st.button(
                    "🗑",
                    key=f"del_{idx}"
                ):

                    delete_recommendation(
                        idx
                    )

                    st.rerun()

        if st.button(
            "🗑 보관함 전체 삭제"
        ):

            delete_all_recommendations()

            st.success(
                "보관함 삭제 완료"
            )

            st.rerun()        

def analyze_winner_patterns(lotto_df):

    rows = []

    for _, row in lotto_df.iterrows():

        nums = sorted([

            row["번호1"],
            row["번호2"],
            row["번호3"],
            row["번호4"],
            row["번호5"],
            row["번호6"]

        ])

        odd = sum(
            1 for n in nums
            if n % 2 == 1
        )

        even = 6 - odd

        low = sum(
            1 for n in nums
            if n <= 22
        )

        high = 6 - low

        consecutive = 0

        for i in range(5):

            if nums[i] + 1 == nums[i + 1]:
                consecutive += 1

        same_end = (
            len(nums)
            -
            len(set(n % 10 for n in nums))
        )

        rows.append({

            "sum": sum(nums),
            "odd": odd,
            "even": even,
            "low": low,
            "high": high,
            "consecutive": consecutive,
            "same_end": same_end

        })

    return pd.DataFrame(rows)

from collections import Counter

def get_number_frequency(df):

    counter = Counter()

    for numbers in df["numbers"]:

        nums = list(
            map(
                int,
                numbers.split(",")
            )
        )

        counter.update(nums)

    freq_df = pd.DataFrame({

        "번호": list(counter.keys()),
        "출현횟수": list(counter.values())

    })

    freq_df = freq_df.sort_values(
        "출현횟수",
        ascending=False
    )

    return freq_df

def rebuild_cache_only():

    lotto_df = get_lotto_history()

    pair_count = save_pair_cache(
        lotto_df
    )

    triple_count = save_triple_cache(
        lotto_df
    )

    return pair_count, triple_count