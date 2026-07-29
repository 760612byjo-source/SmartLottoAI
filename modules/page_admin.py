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
    show_window_patterns
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

            lotto_df = pd.read_excel(
                "data/lotto_history.xlsx"
            )

            patterns = build_window_patterns(
                lotto_df
            )

            show_window_patterns(
                patterns
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

def rebuild_cache_only():

    lotto_df = pd.read_excel(
        "data/lotto_history.xlsx"
    )

    st.write(lotto_df.columns.tolist())

    pair_count = save_pair_cache(
        lotto_df
    )

    triple_count = save_triple_cache(
        lotto_df
    )

    return pair_count, triple_count