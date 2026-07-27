# modules/page_admin.py

import streamlit as st

from modules.update_manager import (
    run_full_update,
    get_update_status,
    get_cache_status,
    get_missing_draws
)


def show_admin_page():

    st.title("⚙️ 시스템 관리")

    st.markdown("---")

    status = get_update_status()
    cache_info = get_cache_status()

    missing_draws = get_missing_draws()


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

    else:

        st.success(
            "✅ 최신 상태"
        )

    if st.button(
        "🔄 최신 데이터 업데이트",
        use_container_width=True
    ):

        with st.spinner("업데이트 진행 중..."):

            logs = run_full_update()

        st.success("업데이트 완료")

        for log in logs:
            st.write(log)

    if missing_draws:

        preview = ", ".join(
            map(
                str,
                missing_draws[:10]
            )
        )

        st.caption(
            f"누락 회차 예시 : {preview} ..."
        )