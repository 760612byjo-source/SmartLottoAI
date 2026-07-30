import streamlit as st
import pandas as pd
import plotly.express as px

from modules.home_page import (
    show_home
)

from modules.data_loader import (
    get_excel_files,
    get_sheet_names,
    load_sheet
)

from modules.lotto_db import (
    get_lotto_history
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

from modules.lotto_analysis import (
    get_recent_df,
    get_missing_df
)

from modules.page_generator import (
    show_generator_page
)

from modules.page_dashboard import (
    show_dashboard_page
)

from modules.page_lotto_db import (
    show_lotto_db_page
)

from modules.page_file_analysis import (
    show_file_analysis_page
)

from modules.backtest_engine import (
    run_backtest
)

from modules.page_backtest import (
    show_backtest_page
)

from modules.adaptive_engine import (
    load_adaptive_weights,
    initialize_adaptive_weights
)

from modules.page_adaptive import (
    show_adaptive_page
)    

from modules.pair_builder import (
    save_pair_cache
)

from modules.triple_engine import (
    build_triple_frequency,
    calculate_triple_score
)

from modules.pattern_engine import (
    build_multi_window_stats,
    calculate_pattern_score
)

from modules.page_admin import show_admin_page

st.set_page_config(
    page_title="LAI",
    page_icon="🎱",
    layout="wide"
)

from modules.update_manager import (
    get_update_status
)

st.title("🎱 LAI")

st.markdown("---")

lotto = get_lotto_history()

weights = load_adaptive_weights()

if weights is None:

    initialize_adaptive_weights(
        lotto
    )

status = get_update_status()

st.sidebar.markdown("---")

if status["need_update"]:

    st.sidebar.warning(
        f"""
🟡 업데이트 필요

DB : {status['db_draw']}회
최신 : {status['latest_draw']}회
"""
    )

    st.sidebar.caption(
        "Admin → 전체 업데이트 실행"
    )

else:

    st.sidebar.success(
        f"""
🟢 DB 최신 상태

현재 : {status['db_draw']}회
"""
    )

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "메뉴",
    [
        "홈",
        "파일 분석",
        "로또DB",
        "번호생성",
        "통계대시보드",
        "백테스트",
        "Adaptive",
        "Pair Engine",
        "Admin"
    ]
)

# ============================
# 홈
# ============================

if menu == "홈":

    show_home()

# ============================
# 파일 분석
# ============================

elif menu == "파일 분석":

    show_file_analysis_page()

# =========================
# 로또 DB
# =========================

elif menu == "로또DB":

    show_lotto_db_page()

# ==========================
# 번호 생성
# ==========================

elif menu == "번호생성":

    show_generator_page()

# ==========================
# 통계 대시보드
# ==========================

elif menu == "통계대시보드":

    show_dashboard_page()

# ==========================
# 백테스트
# ==========================

elif menu == "백테스트":

    show_backtest_page()

# ==========================
# Adaptive
# ==========================

elif menu == "Adaptive":

    show_adaptive_page()

# ==========================
# Pair Engine
# ==========================

elif menu == "Pair Engine":

    st.subheader(
        "🎯 Pair Engine"
    )

    if st.button(
        "Pair Cache 생성"
    ):

        count = save_pair_cache(
            lotto
        )

        st.success(
            f"{count:,}개 번호쌍 저장 완료"
        )
# ==========================
# Admin
# ==========================

elif menu == "Admin":
    show_admin_page()