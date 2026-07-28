# modules/update_manager.py

import pandas as pd
from datetime import datetime

from modules.pair_builder import save_pair_cache
from modules.lotto_updater import (
    update_lotto_history,
    fetch_draw_data
)
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

        result = append_missing_draws()

        logs.append(
            f"📥 자동 보충 성공 : "
            f"{result['success']}회"
        )

        logs.append(
            f"❌ 실패 : "
            f"{len(result['failed'])}회"
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
    #try:

        # count = build_lotto_history()

        # logs.append(
        #     f"✅ lotto_history 생성 완료 ({count}회)"
        # )

    #except Exception as e:

        #logs.append(
            #f"❌ lotto_history 생성 실패 : {e}"
        #)

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
        "data/lotto_history.xlsx"
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

def load_update_status_log():

    try:

        with open(
            "data/update_status.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return None

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

    print("MISSING LATEST =", latest_draw)

    return list(
        range(
            db_draw + 1,
            latest_draw + 1
        )
    )

def append_missing_draws():
    
    missing_draws = get_missing_draws()

    success_count = 0

    failed = []

    history_df = pd.read_excel(
        "data/lotto_history.xlsx"
    )

    for draw_no in missing_draws:
        
        row = fetch_draw_data(draw_no)

        if row:

            history_df.loc[
                len(history_df)
            ] = [
                row["회차"],
                row["추첨일"],
                row["1열"],
                row["2열"],
                row["3열"],
                row["4열"],
                row["5열"],
                row["6열"],
                row["보너스"]
            ]

            success_count += 1

        else:

            failed.append(draw_no)

    history_df = history_df.sort_values(
        "회차"
    )
        
    history_df.to_excel(
        "data/lotto_history.xlsx",
        index=False
    )

    latest_draw = int(
        history_df["회차"].max()
    )

    save_update_status_log(
        latest_draw=latest_draw,
        success_count=success_count,
        failed_count=len(failed),
        missing_count=len(missing_draws)
    )

    return {
        "success": success_count,
        "failed": failed
    }


def save_update_status_log(
    latest_draw,
    success_count,
    failed_count,
    missing_count
):

    status = {

        "last_update":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "latest_draw":
            latest_draw,

        "success_count":
            success_count,

        "failed_count":
            failed_count,

        "missing_count":
            missing_count
    }

    with open(
        "data/update_status.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            status,
            f,
            ensure_ascii=False,
            indent=4
        )

