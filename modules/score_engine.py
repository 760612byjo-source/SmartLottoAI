from modules.adaptive_engine import (
    get_adaptive_weights
)

def calculate_score(
    numbers,
    include_numbers,
    hot_numbers,
    missing_numbers
):

    score = 0

    weights = get_adaptive_weights()

    if weights is None:
        return 0

    # 포함수
    include_count = len(
        set(numbers)
        & set(include_numbers)
    )

    score += include_count * 10

    # 강세수
    hot_count = len(
        set(numbers)
        & set(hot_numbers)
    )

    score += hot_count * 10

    # 장기미출현수
    missing_count = len(
        set(numbers)
        & set(missing_numbers)
    )

    score += missing_count * 4

    # 홀짝 패턴
    odd_count = sum(
        n % 2 == 1
        for n in numbers
    )

    even_count = 6 - odd_count

    odd_pattern = (
        f"{odd_count}:{even_count}"
    )

    score += (
        weights["odd_even"]
        .get(odd_pattern, 0)
    )

    # 저고 패턴
    low_count = sum(
        n <= 22
        for n in numbers
    )

    high_count = 6 - low_count

    low_pattern = (
        f"{low_count}:{high_count}"
    )

    score += (
        weights["low_high"]
        .get(low_pattern, 0)
    )

    # 소수 패턴
    PRIMES = [
        2, 3, 5, 7,
        11, 13, 17, 19,
        23, 29, 31, 37,
        41, 43
    ]

    prime_count = sum(
        n in PRIMES
        for n in numbers
    )

    score += (
        weights["prime"]
        .get(str(prime_count), 0)
    )

    # 연속수
    consecutive = 0

    sorted_nums = sorted(numbers)

    for i in range(
        len(sorted_nums) - 1
    ):

        if (
            sorted_nums[i + 1]
            -
            sorted_nums[i]
            == 1
        ):
            consecutive += 1

    if consecutive == 1:

        score += 5

    elif consecutive >= 2:

        score += 3

    # 번호합
    total = sum(numbers)

    if 100 <= total <= 180:

        score += 10

    elif 90 <= total <= 190:

        score += 5

    # 끝수합
    end_sum = sum(
        n % 10
        for n in numbers
    )

    bucket = (
        end_sum // 5
    ) * 5

    score += (
        weights["endsum"]
        .get(str(bucket), 0)
    )

    # 삼그룹
    group1 = sum(
        1 <= n <= 15
        for n in numbers
    )

    group2 = sum(
        16 <= n <= 30
        for n in numbers
    )

    group3 = sum(
        31 <= n <= 45
        for n in numbers
    )

    group_pattern = (
        f"{group1}:{group2}:{group3}"
    )

    score += (
        weights.get(
            "three_group",
            {}
        ).get(
            group_pattern,
            0
        )
    )

    # 구간분산
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

    if max(sections) <= 2:

        score += 10

    elif max(sections) <= 3:

        score += 5

    # 끝수분산
    endings = [
        n % 10
        for n in numbers
    ]

    score += len(
        set(endings)
    )

    # 중복 끝수 감점
    duplicate_endings = (
        len(endings)
        -
        len(set(endings))
    )

    score -= duplicate_endings

    return score
