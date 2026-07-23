import pandas as pd
from pathlib import Path

DATA_FILE = Path("data/3.집계.xlsm")


def load_lotto_db():

    df = pd.read_excel(
        DATA_FILE,
        sheet_name="집계",
        header=None
    )

    return df


def get_lotto_history():

    df = load_lotto_db()

    # 실제 데이터 부분
    lotto = df.iloc[3:].copy()

    lotto = lotto.iloc[:, :20]

    lotto.columns = [
        "년도",
        "회차",
        "추첨일",
        "1등당첨자",
        "1등금액",
        "2등당첨자",
        "2등금액",
        "3등당첨자",
        "3등금액",
        "4등당첨자",
        "4등금액",
        "5등당첨자",
        "5등금액",
        "번호1",
        "번호2",
        "번호3",
        "번호4",
        "번호5",
        "번호6",
        "보너스"
    ]

    lotto["회차"] = pd.to_numeric(
        lotto["회차"],
        errors="coerce"
    )

    # 회차가 없는 행 제거
    lotto = lotto.dropna(
        subset=["회차"]
    )

    lotto = lotto.sort_values(
        "회차"
    )

    lotto = lotto.reset_index(
        drop=True
    )

    return lotto