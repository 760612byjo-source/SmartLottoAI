import pandas as pd
import streamlit as st

from collections import Counter


PRIMES = {
    2, 3, 5, 7,
    11, 13, 17, 19,
    23, 29, 31, 37,
    41, 43
}


NUMBER_COLS = [
    "번호1",
    "번호2",
    "번호3",
    "번호4",
    "번호5",
    "번호6"
]


def odd_even_pattern(numbers):

    odd = sum(
        n % 2 == 1
        for n in numbers
    )

    even = 6 - odd

    return f"{odd}:{even}"


def low_high_pattern(numbers):

    low = sum(
        n <= 22
        for n in numbers
    )

    high = 6 - low

    return f"{low}:{high}"


def prime_pattern(numbers):

    return sum(
        n in PRIMES
        for n in numbers
    )


def endsum_pattern(numbers):

    return sum(
        n % 10
        for n in numbers
    )


def three_group_pattern(numbers):

    g1 = sum(
        1 <= n <= 15
        for n in numbers
    )

    g2 = sum(
        16 <= n <= 30
        for n in numbers
    )

    g3 = sum(
        31 <= n <= 45
        for n in numbers
    )

    return f"{g1}:{g2}:{g3}"

def sum_pattern(numbers):

    total = sum(numbers)

    bucket = (
        total // 10
    ) * 10

    return bucket

def section_pattern(numbers):

    sections = [0, 0, 0, 0, 0]

    for n in numbers:

        if n <= 10:

            sections[0] += 1

        elif n <= 20:

            sections[1] += 1

        elif n <= 30:

            sections[2] += 1

        elif n <= 40:

            sections[3] += 1

        else:

            sections[4] += 1

    return ":".join(
        map(str, sections)
    )

def ending_pattern(numbers):

    endings = [
        n % 10
        for n in numbers
    ]

    counts = [0] * 10

    for e in endings:

        counts[e] += 1

    return ":".join(
        map(str, counts)
    )

def consecutive_pattern(numbers):

    numbers = sorted(numbers)

    consecutive = 0

    for i in range(5):

        if numbers[i + 1] - numbers[i] == 1:

            consecutive += 1

    return consecutive

def extract_top_patterns(
    lotto_df,
    window=27,
    top_n=4
):

    df = lotto_df.tail(window)

    odd_even_counter = Counter()
    low_high_counter = Counter()
    prime_counter = Counter()
    endsum_counter = Counter()
    group_counter = Counter()
    sum_counter = Counter()
    section_counter = Counter()
    ending_counter = Counter()  
    consecutive_counter = Counter()

    for _, row in df.iterrows():

        numbers = [
            int(row[col])
            for col in NUMBER_COLS
        ]

        odd_even_counter[
            odd_even_pattern(numbers)
        ] += 1

        low_high_counter[
            low_high_pattern(numbers)
        ] += 1

        prime_counter[
            prime_pattern(numbers)
        ] += 1

        endsum_counter[
            endsum_pattern(numbers)
        ] += 1

        group_counter[
            three_group_pattern(numbers)
        ] += 1

        sum_counter[
            sum_pattern(numbers)
        ] += 1

        section_counter[
            section_pattern(numbers)
        ] += 1

        ending_counter[
            ending_pattern(numbers)
        ] += 1

        consecutive_counter[
            consecutive_pattern(numbers)
        ] += 1

    return {

        "odd_even": [
            x[0]
            for x in odd_even_counter.most_common(top_n)
        ],

        "low_high": [
            x[0]
            for x in low_high_counter.most_common(top_n)
        ],

        "prime": [
            x[0]
            for x in prime_counter.most_common(top_n)
        ],

        "endsum": [
            x[0]
            for x in endsum_counter.most_common(top_n)
        ],

        "three_group": [
            x[0]
            for x in group_counter.most_common(top_n)
        ],

        "sum": [
            x[0]
            for x in sum_counter.most_common(top_n)
        ],

        "section": [
            x[0]
            for x in section_counter.most_common(top_n)
        ],

        "ending": [
            x[0]
            for x in ending_counter.most_common(top_n)
        ],

        "consecutive": [
            x[0]
            for x in consecutive_counter.most_common(top_n)
        ]
    }


def build_window_patterns(
    lotto_df
):

    return {

        "27W":
        extract_top_patterns(
            lotto_df,
            27,
            4
        ),

        "20W":
        extract_top_patterns(
            lotto_df,
            20,
            4
        ),

        "10W":
        extract_top_patterns(
            lotto_df,
            10,
            4
        )
    }


def show_window_patterns(
    window_patterns
):

    st.subheader(
        "🏆 Multi-Window Pattern 분석"
    )

    for window in [
        "27W",
        "20W",
        "10W"
    ]:

        data = window_patterns[window]

        df = pd.DataFrame({

            "패턴": [
                "홀짝",
                "저고",
                "소수",
                "끝수합",
                "삼그룹",
                "번호합",
                "구간분산",
                "끝수분산",
                "연속수"        
            ],

            "TOP4": [
                ", ".join(map(str, data["odd_even"])),
                ", ".join(map(str, data["low_high"])),
                ", ".join(map(str, data["prime"])),
                ", ".join(map(str, data["endsum"])),
                ", ".join(map(str, data["three_group"])),
                ", ".join(map(str, data["sum"])),
                ", ".join(map(str, data["section"])),
                ", ".join(map(str, data["ending"])),
                ", ".join(map(str, data["consecutive"]))
            ]
        })

        st.markdown(
            f"### {window}"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

WINDOW_SCORE = {
    "27W": 1,
    "20W": 1,
    "10W": 1
}


def calculate_window_pattern_score(
    numbers,
    window_patterns
):

    score = 0

    odd_even = odd_even_pattern(numbers)

    low_high = low_high_pattern(numbers)

    prime = prime_pattern(numbers)

    endsum = endsum_pattern(numbers)

    group = three_group_pattern(numbers)

    sum_value = sum_pattern(numbers)

    section = section_pattern(numbers)

    ending = ending_pattern(numbers)

    consecutive = consecutive_pattern(numbers)

    for window in [
        "27W",
        "20W",
        "10W"
    ]:

        weight = WINDOW_SCORE[window]

        if odd_even in window_patterns[window]["odd_even"]:
            score += weight

        if low_high in window_patterns[window]["low_high"]:
            score += weight

        if prime in window_patterns[window]["prime"]:
            score += weight

        if endsum in window_patterns[window]["endsum"]:
            score += weight

        if group in window_patterns[window]["three_group"]:
            score += weight

        if sum_value in window_patterns[window]["sum"]:
            score += weight

        if section in window_patterns[window]["section"]:
            score += weight

        if ending in window_patterns[window]["ending"]:
            score += weight

        if consecutive in window_patterns[window]["consecutive"]:
            score += weight

    return score