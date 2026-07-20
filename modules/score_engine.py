def calculate_score(
    numbers,
    include_numbers,
    hot_numbers,
    missing_numbers
):

    score = 0

    # 포함수

    include_count = len(
        set(numbers)
        &
        set(include_numbers)
    )

    score += include_count * 10

    # 강세수

    hot_count = len(
        set(numbers)
        &
        set(hot_numbers)
    )

    score += hot_count * 5

    # 장기미출현수

    missing_count = len(
        set(numbers)
        &
        set(missing_numbers)
    )

    score += missing_count * 5

    return score