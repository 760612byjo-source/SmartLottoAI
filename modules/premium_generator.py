import random


def generate_premium_numbers(
    core_numbers,
    missing_numbers,
    count=5
):

    results = []

    while len(results) < count:

        selected_core = random.sample(
            core_numbers,
            4
        )

        available_missing = [
            n
            for n in missing_numbers
            if n not in selected_core
        ]

        if len(available_missing) < 2:
            continue

        remain = random.sample(
            available_missing,
            2
        )

        numbers = sorted(
            selected_core + remain
        )

        if numbers not in results:

            results.append(
                numbers
            )

    return results