import random

# -------------------------
# 부모 선택
# -------------------------

def select_parents(scored_numbers, top_n=50):

    scored_numbers = sorted(
        scored_numbers,
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_numbers[:top_n]


# -------------------------
# 교배
# -------------------------

def crossover(parent1, parent2):

    merged = list(
        set(parent1[:3] + parent2[3:])
    )

    while len(merged) < 6:

        n = random.randint(1, 45)

        if n not in merged:
            merged.append(n)

    merged = sorted(merged[:6])

    return merged


# -------------------------
# 변이
# -------------------------

def mutate(numbers, rate=0.20):

    result = numbers.copy()

    if random.random() < rate:

        idx = random.randint(0, 5)

        while True:

            new_num = random.randint(1, 45)

            if new_num not in result:

                result[idx] = new_num
                break

    return sorted(result)


# -------------------------
# 다음세대 생성
# -------------------------

def create_next_generation(
    elite_numbers,
    offspring_count=500
):

    children = []

    while len(children) < offspring_count:

        p1 = random.choice(elite_numbers)
        p2 = random.choice(elite_numbers)

        child = crossover(
            p1["numbers"],
            p2["numbers"]
        )

        child = mutate(child)

        children.append(child)

    return children
