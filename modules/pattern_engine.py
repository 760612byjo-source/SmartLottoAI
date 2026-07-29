from collections import Counter

WINDOW_WEIGHT = {
    "ALL": 1.0,
    "27W": 1.5,
    "20W": 2.0,
    "10W": 3.0
}


def odd_even_pattern(nums):
    odd = sum(1 for n in nums if n % 2)
    even = 6 - odd
    return f"{odd}:{even}"


def low_high_pattern(nums):
    low = sum(1 for n in nums if n <= 22)
    high = 6 - low
    return f"{low}:{high}"


def prime_pattern(nums):
    primes = {
        2,3,5,7,11,13,17,19,
        23,29,31,37,41,43
    }
    return sum(
        1 for n in nums
        if n in primes
    )


def endsum_pattern(nums):
    return sum(n % 10 for n in nums)


def three_group_pattern(nums):

    g1 = sum(
        1 for n in nums
        if n <= 15
    )

    g2 = sum(
        1 for n in nums
        if 16 <= n <= 30
    )

    g3 = sum(
        1 for n in nums
        if n >= 31
    )

    return f"{g1}-{g2}-{g3}"


def build_pattern_stats(
    lotto_df,
    window=None
):

    if window:
        df = lotto_df.tail(window)
    else:
        df = lotto_df.copy()

    number_cols = [
        "1열","2열","3열",
        "4열","5열","6열"
    ]

    odd_even_counter = Counter()
    low_high_counter = Counter()
    prime_counter = Counter()
    endsum_counter = Counter()
    group_counter = Counter()

    for _, row in df.iterrows():

        nums = [
            int(row[col])
            for col in number_cols
        ]

        odd_even_counter[
            odd_even_pattern(nums)
        ] += 1

        low_high_counter[
            low_high_pattern(nums)
        ] += 1

        prime_counter[
            prime_pattern(nums)
        ] += 1

        endsum_counter[
            endsum_pattern(nums)
        ] += 1

        group_counter[
            three_group_pattern(nums)
        ] += 1

    return {
        "odd_even": dict(odd_even_counter),
        "low_high": dict(low_high_counter),
        "prime": dict(prime_counter),
        "endsum": dict(endsum_counter),
        "group": dict(group_counter),
    }


def build_multi_window_stats(lotto_df):

    return {

        "ALL":
        build_pattern_stats(
            lotto_df
        ),

        "27W":
        build_pattern_stats(
            lotto_df,
            27
        ),

        "20W":
        build_pattern_stats(
            lotto_df,
            20
        ),

        "10W":
        build_pattern_stats(
            lotto_df,
            10
        ),
    }


def calculate_pattern_score(
    numbers,
    multi_stats
):

    score = 0

    odd_even = odd_even_pattern(numbers)
    low_high = low_high_pattern(numbers)
    prime = prime_pattern(numbers)
    endsum = endsum_pattern(numbers)
    group = three_group_pattern(numbers)

    for window, stats in multi_stats.items():

        weight = WINDOW_WEIGHT[window]

        score += (
            stats["odd_even"].get(
                odd_even, 0
            ) * weight
        )

        score += (
            stats["low_high"].get(
                low_high, 0
            ) * weight
        )

        score += (
            stats["prime"].get(
                prime, 0
            ) * weight
        )

        score += (
            stats["endsum"].get(
                endsum, 0
            ) * weight
        )

        score += (
            stats["group"].get(
                group, 0
            ) * weight
        )

    return score
