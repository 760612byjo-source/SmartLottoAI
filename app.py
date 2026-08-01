import streamlit as st
import os

from modules.lotto_db import (
    get_lotto_history
)

from modules.page_generator import (
    show_generator_page
)

from modules.adaptive_engine import (
    load_adaptive_weights,
    initialize_adaptive_weights
)

from modules.page_admin import show_admin_page

st.set_page_config(
    page_title="LAI",
    page_icon="🎱",
    layout="wide",
)

ADMIN_PASSWORD = "1234"

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

    st.sidebar.caption(
        f"LAI Engine v1.0"
    )

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "메뉴",
    [
        "🎯 추천번호 생성",
        "🔐 Admin"
    ]
)

if menu == "🎯 추천번호 생성":

    show_generator_page()

elif menu == "🔐 Admin":

    password = st.text_input(
        "관리자 비밀번호",
        type="password"
    )

    if password == ADMIN_PASSWORD:

        show_admin_page()

    elif password:

        st.error(
            "비밀번호가 올바르지 않습니다."
        )