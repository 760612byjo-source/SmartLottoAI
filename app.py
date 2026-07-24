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
    initialize_adaptive_weights
)

from modules.lotto_db import (
    get_lotto_history
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

st.set_page_config(
    page_title="LAI",
    page_icon="🎱",
    layout="wide"
)

st.title("🎱 LAI")

st.markdown("---")

lotto = get_lotto_history()

weights = load_adaptive_weights()

if weights is None:

    initialize_adaptive_weights(
        lotto
    )

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
        "Pair Engine"
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

if menu == "파일 분석":

    show_file_analysis_page()

# =========================
# 로또 DB
# =========================

if menu == "로또DB":

    show_lotto_db_page()

# ==========================
# 번호 생성
# ==========================

if menu == "번호생성":

    show_generator_page()

# ==========================
# 통계 대시보드
# ==========================

if menu == "통계대시보드":

    show_dashboard_page()

# ==========================
# 백테스트
# ==========================

if menu == "백테스트":

    show_backtest_page()

# ==========================
# Adaptive
# ==========================

if menu == "Adaptive":

    show_adaptive_page()

# ==========================
# Pair Engine
# ==========================

if menu == "Pair Engine":

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