import random

from modules.score_engine import (
    calculate_score
)

def create_number_set():

    numbers = random.sample(
        range(1, 46),
        6
    )

    numbers.sort()

    return numbers


def odd_even_check(numbers):

    odd = sum(
        n % 2 == 1
        for n in numbers
    )

    even = 6 - odd

    return (
        (odd == 3 and even == 3)
        or
        (odd == 4 and even == 2)
        or
        (odd == 2 and even == 4)
    )


def low_high_check(numbers):

    low = sum(
        n <= 22
        for n in numbers
    )

    high = 6 - low

    return (
        (low == 3 and high == 3)
        or
        (low == 4 and high == 2)
        or
        (low == 2 and high == 4)
    )


def end_sum_check(numbers):

    end_sum = sum(
        n % 10
        for n in numbers
    )

    return 20 <= end_sum <= 35


def prime_check(numbers):

    primes = {
        2, 3, 5, 7,
        11, 13, 17, 19,
        23, 29, 31, 37,
        41, 43
    }

    prime_count = sum(
        n in primes
        for n in numbers
    )

    return 1 <= prime_count <= 4


def exclude_check(
    numbers,
    exclude_numbers
):

    return len(
        set(numbers) &
        set(exclude_numbers)
    ) == 0


def include_check(
    numbers,
    include_numbers
):

    count = len(
        set(numbers) &
        set(include_numbers)
    )

    return count >= 2


def generate_numbers(
    exclude_numbers,
    include_numbers,
    hot_numbers,
    missing_numbers,
    count=10
):

    results = []

    attempts = 0

    while len(results) < count:

        attempts += 1

        if attempts > 50000:
            break

        numbers = create_number_set()

        if not odd_even_check(numbers):
            continue

        if not low_high_check(numbers):
            continue

        if not end_sum_check(numbers):
            continue

        if not prime_check(numbers):
            continue

        if not exclude_check(
            numbers,
            exclude_numbers
        ):
            continue

        if not include_check(
            numbers,
            include_numbers
        ):
            continue

        if numbers not in [
            item["numbers"]
            for item in results
        ]:

            score = calculate_score(
                numbers,
                include_numbers,
                hot_numbers,
                missing_numbers
            )


            results.append(
                {
                    "numbers": numbers,
                    "score": score
                }
            )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results

print("V2.5 number_generator loaded")