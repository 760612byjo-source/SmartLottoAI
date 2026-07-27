# modules/update_manager.py

import pandas as pd
from datetime import datetime

from modules.pair_builder import save_pair_cache
from modules.lotto_updater import update_lotto_history
from modules.triple_builder import (
    save_triple_cache
)

import json

def get_cache_status():

    try:

        with open(
            "data/pair_cache.json",
            "r",
            encoding="utf-8"
        ) as f:

            pair_count = len(
                json.load(f)
            )

    except:

        pair_count = 0

    try:

        with open(
            "data/triple_cache.json",
            "r",
            encoding="utf-8"
        ) as f:

            triple_count = len(
                json.load(f)
            )

    except:

        triple_count = 0

    return {
        "pair_count": pair_count,
        "triple_count": triple_count
    }

def build_lotto_history():

    lotto_df = pd.read_excel(
        "data/3.집계.xlsm",
        header=3
    )

    history_df = lotto_df[
        [
            "회차",
            "추첨일",
            "1열",
            "2열",
            "3열",
            "4열",
            "5열",
            "6열",
            "보너스"
        ]
    ].copy()

    # 회차가 없는 행 제거
    history_df = history_df.dropna(
        subset=["회차"]
    )

    # 숫자로 변환
    history_df["회차"] = pd.to_numeric(
        history_df["회차"],
        errors="coerce"
    )

    # 회차 없는 행 제거
    history_df = history_df.dropna(
        subset=["회차"]
    )

    # 정수형 변환
    history_df["회차"] = (
        history_df["회차"]
        .astype(int)
    )

    history_df.to_excel(
        "data/lotto_history.xlsx",
        index=False
    )

    return len(history_df)

def run_full_update():

    logs = []

    try:

        added_count = append_missing_draws()

        logs.append(
            f"📥 자동 보충 대상 : {added_count}회"
        )

    except Exception as e:

        logs.append(
            f"❌ 자동 보충 오류 : {e}"
        )

    missing_draws = get_missing_draws()

    logs.append(
        f"📥 누락 회차 : {len(missing_draws)}회"
    )

    if missing_draws:

        logs.append(
            f"📋 대상 범위 : "
            f"{missing_draws[0]}회 ~ "
            f"{missing_draws[-1]}회"
        )

    # lotto_history 생성
    try:

        count = build_lotto_history()

        logs.append(
            f"✅ lotto_history 생성 완료 ({count}회)"
        )

    except Exception as e:

        logs.append(
            f"❌ lotto_history 생성 실패 : {e}"
        )

    # Pair Cache 생성
    try:

        lotto_df = pd.read_excel(
            "data/lotto_history.xlsx"
        )

        pair_count = save_pair_cache(
            lotto_df
        )

        logs.append(
            f"✅ Pair Cache 갱신 완료 ({pair_count:,}개)"
        )

    except Exception as e:

        logs.append(
            f"❌ Pair Cache 오류 : {e}"
        )


    
    try:

        lotto_df = pd.read_excel(
            "data/lotto_history.xlsx"
        )

        triple_count = save_triple_cache(
            lotto_df
        )

        logs.append(
            f"✅ Triple Cache 갱신 완료 ({triple_count:,}개)"
        )

    except Exception as e:

        logs.append(
            f"❌ Triple Cache 오류 : {e}"
        )

    logs.append(
        f"🕒 완료 : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    return logs


def get_update_status():

    lotto_df = pd.read_excel(
        "data/3.집계.xlsm",
        header=3
    )

    db_draw = int(
        lotto_df["회차"].max()
    )

    latest_draw = update_lotto_history()

    return {
        "db_draw": db_draw,
        "latest_draw": latest_draw,
        "need_update": latest_draw > db_draw
    }

def get_missing_draws():

    try:

        lotto_df = pd.read_excel(
            "data/lotto_history.xlsx"
        )

        db_draw = int(
            lotto_df["회차"].max()
        )

    except:

        db_draw = 0

    latest_draw = update_lotto_history()

    return list(
        range(
            db_draw + 1,
            latest_draw + 1
        )
    )

def append_missing_draws():

    missing_draws = get_missing_draws()

    return len(missing_draws)