import random as rd

import numpy as np
import numpy.random as random
import pandas as pd


def gen_pattern(pattern_length):
    """gen_pattern

    Parameters
    ----------
    pattern_length : int
            The length of the periodicity pattern

    Returns
    -------
    list
            A pattern to use for periodic data synthesis
    """
    random.seed(rd.randint(0, 10000))
    o = [random.randint(15, 35)]
    o.extend(o[-1] + random.normal(0, 1) for _ in range(pattern_length))
    return o


def join_sequence(l1, l2, n, noise):
    """Join 2 sequences with noisy data.

    Parameters
    ----------
    l1 : float
        Last of first sequence
    l2 : float
        Last of second sequence
    n : int
        How many data points in between

    Returns
    -------
    list
        A joiner to use for periodic data synthesis
    """
    return (np.linspace(l1, l2, n) + random.normal(0, noise, n)).tolist()


def synthesise(length, pattern_length):

    pattern = gen_pattern(pattern_length)  # periodic pattern
    o = [
        pattern[0]
    ]  # to stop error around line: "o = [*o, *join_sequence(o[-1], to_add[0], 15, 3), *to_add.tolist()]"

    for _ in range(length):  # time complexity O(n) = n^2
        to_add = []  # generate data that allows for noise input
        for i in pattern:
            to_add.extend(i for _ in range(3))
        shift = random.normal(
            0, 3
        )  # how much each periodic interval should be shifted up/down
        to_add = (
            np.array(to_add)
            + random.normal(0, 0.2, len(to_add))  # add noise
            + np.array([shift for _ in range(len(to_add))])  # add shift
        )
        o = [
            *o,
            *join_sequence(o[-1], to_add[0], 10, 0.2),
            *to_add.tolist(),
        ]  # append to end of output o

    print("Generated data with length ", len(o))

    return o


if __name__ == "__main__":
    choices = [  # params to ensure that all data points have same length
        (2, 180),
        (3, 120),
        (4, 90),
        (5, 72),
        (6, 60),
        (8, 45),
        (9, 40),
        (10, 36),
    ]

    x = [synthesise(*rd.choice(choices)) for _ in range(1000)]
    min_len = min(len(i) for i in x)

    x = [i[: min_len - 1] for i in x]

    x = np.array(x)
    x = pd.DataFrame(x)
    x.index.name = "id"
    x.dropna(axis=1, inplace=True)
    x.to_csv("data/synthesised.csv")
