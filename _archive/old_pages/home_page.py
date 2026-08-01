import streamlit as st


def show_home():

    st.subheader("프로젝트 현황")

    st.success(
        "SmartLottoAI 개발 진행 중"
    )

    st.write("✅ 엑셀 통합")
    st.write("✅ 파일 분석")
    st.write("✅ 로또DB 구축")
    st.write("✅ 홀짝 분석")
    st.write("✅ 저고 분석")
    st.write("✅ 끝수 분석")
    st.write("✅ 소수 분석")
    st.write("✅ 최근출현수 분석")
    st.write("✅ 장기미출현수 분석")
    st.write("✅ 제외수 엔진")
    st.write("✅ 포함수 엔진")
    st.write("✅ 번호 생성 엔진")
    st.write("✅ 점수 기반 추천")
    st.write("✅ 통계 대시보드")

    st.markdown("---")

    st.subheader("현재 버전")

    st.info(
        "SmartLottoAI V2.6"
    )

    st.markdown("---")

    st.subheader("개발 로드맵")

    st.write("V2.6 ✅ 통계대시보드")
    st.write("V2.7 🔄 성능검증 시스템")
    st.write("V2.8 🔄 번호추천 고도화")
    st.write("V3.0 🔄 AI 예측 엔진")

    st.markdown("---")

    st.subheader("현재 기능")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            📊 분석 기능

            • 출현빈도 분석
            • 홀짝 분석
            • 저고 분석
            • 끝수 분석
            • 소수 분석
            • 강세수 분석
            • 미출현수 분석
            """
        )

    with col2:

        st.info(
            """
            🎯 추천 기능

            • 제외수 적용
            • 포함수 적용
            • 추천번호 생성
            • 점수 계산
            • 순위 정렬
            • TOP 추천번호 제공
            """
        )