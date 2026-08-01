import streamlit as st

from modules.data_loader import (
    get_excel_files,
    get_sheet_names,
    load_sheet
)


def show_file_analysis_page():

    files = get_excel_files()

    if len(files) == 0:

        st.warning(
            "data 폴더에 파일이 없습니다."
        )

    else:

        selected_file = st.selectbox(
            "파일 선택",
            files
        )

        sheets = get_sheet_names(
            selected_file
        )

        selected_sheet = st.selectbox(
            "시트 선택",
            sheets
        )

        df = load_sheet(
            selected_file,
            selected_sheet
        )

        st.subheader(
            "데이터 미리보기"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )

        st.subheader(
            "상위 20행"
        )

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "데이터 정보"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "행 개수",
                len(df)
            )

        with col2:
            st.metric(
                "열 개수",
                len(df.columns)
            )

        with col3:
            st.metric(
                "파일",
                selected_file
            )