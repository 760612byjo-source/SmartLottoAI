import requests


def get_latest_draw(draw_no):

    url = (
        "https://www.dhlottery.co.kr/"
        "lt645/selectPstLt645InfoNew.do"
    )

    params = {
        "srchDir": "center",
        "srchLtEpsd": draw_no
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def update_lotto_history():

    try:

        data = get_latest_draw(1234)

        rows = data["data"]["list"]

        if not rows:
            return 0

        return int(
            rows[0]["ltEpsd"]
        )   

    except Exception as e:

        print(
            f"최신 회차 조회 실패 : {e}"
        )

        return 0

def get_draw_data(draw_no):

    return {
        "회차": draw_no,
        "추첨일": "",
        "1열": 0,
        "2열": 0,
        "3열": 0,
        "4열": 0,
        "5열": 0,
        "6열": 0,
        "보너스": 0
    }


def fetch_draw_data(draw_no):

    try:

        data = get_latest_draw(draw_no)

        rows = data["data"]["list"]

        if not rows:
            return None

        row = None

        for item in rows:

            if item["ltEpsd"] == draw_no:

                row = item

                break

        if row is None:

            print(
                f"회차를 찾을 수 없음 : {draw_no}"
            )

            return None

        return {
            "회차": row["ltEpsd"],
            "추첨일": row["ltRflYmd"],
            "1열": row["tm1WnNo"],
            "2열": row["tm2WnNo"],
            "3열": row["tm3WnNo"],
            "4열": row["tm4WnNo"],
            "5열": row["tm5WnNo"],
            "6열": row["tm6WnNo"],
            "보너스": row["bnsWnNo"]
        }

    except Exception as e:

        print(
            f"조회 실패 : {draw_no}회"
        )

        print(e)

        return None
    
        
if __name__ == "__main__":

    print(
        update_lotto_history()
    )