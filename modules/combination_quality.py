def evaluate_combination(numbers):

    score = 0

    nums = sorted(numbers)

    # 홀짝

    odd_count = len(
        [n for n in nums if n % 2 == 1]
    )

    even_count = 6 - odd_count

    if odd_count in [2, 3, 4]:
        score += 10

    # 고저

    low_count = len(
        [n for n in nums if n <= 22]
    )

    high_count = 6 - low_count

    if low_count in [2, 3, 4]:
        score += 10

    # 연번

    consecutive = 0

    for i in range(5):

        if nums[i+1] - nums[i] == 1:
            consecutive += 1

    if consecutive == 0:
        score += 10

    elif consecutive == 1:
        score += 5

    else:
        score -= 10

    return score

def get_historical_penalty(
    numbers,
    lotto_df
):

    score = 0

    candidate = set(numbers)

    for _, row in lotto_df.iterrows():

        winner = {
            row["1열"],
            row["2열"],
            row["3열"],
            row["4열"],
            row["5열"],
            row["6열"]
        }

        hit = len(
            candidate & winner
        )

        if hit >= 5:

            score += 100

        elif hit == 4:

            score += 20

    return score