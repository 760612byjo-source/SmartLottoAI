from collections import Counter

from collections import Counter


def get_core_numbers(
    results,
    top_n=6
):

    counter = Counter()

    for item in results:

        for n in item["numbers"]:

            counter[n] += 1

    return [
        num
        for num, _
        in counter.most_common(top_n)
    ]


def get_consensus_numbers(results):

    counter = Counter()

    for item in results:

        for n in item["numbers"]:

            counter[n] += 1

    return counter.most_common()