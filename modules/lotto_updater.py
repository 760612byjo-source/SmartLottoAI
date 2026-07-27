import requests


def get_latest_draw(draw_no):

    url = (
        "https://www.dhlottery.co.kr/common.do"
        f"?method=getLottoNumber&drwNo={draw_no}"
    )

    response = requests.get(url)

    return response.json()


def update_lotto_history():
    return 1196


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

def append_missing_draws():

    missing_draws = get_missing_draws()

    if not missing_draws:
        return 0

    count = 0

    for draw_no in missing_draws:

        # 여기서 회차 데이터 수집
        # lotto_history.xlsx 추가

        count += 1

    return count