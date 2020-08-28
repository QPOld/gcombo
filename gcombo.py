r"""
Module      : GCombo
Description : The fastest powerset generator for python.
Copyright   : (c) Michael Parkinson, 2020
License     : GPL-3
Maintainer  : mqparkinson@gmail.com
Stability   : experimental
Portability : POSIX

This module provides the functionality to generate a powerset from the
finite set of integers [1..N].
"""


def gcombo(base: int, length: int) -> list:
    r"""
    Split the length in half and use algorithm H to calculate all
    sets with cardinality of length / 2. Find all sets in base 2^(l/2) with
    length 2 and use it to map the length / 2 set into the length set.

    Input:
        - base {integer} The largest integer to occur in each combination.
        - length {integer} The length of each combinaton.

    Output: A list of every possible combination.
    """
    every_solution = []  # Delete for no store.

    if length % 2 != 0:
        _l = (length-1) // 2
        _one = _product([base for i in range(1)])
    else:
        _l = length // 2
        _one = [[]]

    _h = _product([base for i in range(_l)])  # Calc the half set _h
    _b = pow(base, _l)  # New base _b

    # Simple for loops
    for i in range(_b):
        for j in range(_b):
            for k in range(len(_one)):
                # Yield solution
                solution = _h[j] + _h[i] + _one[k]

                # Append solution
                every_solution.append(solution)

    return every_solution


def _product(m: list) -> list:
    r"""
    Iterator over the switch for the iteration of the product
    `[m_0] \times [m_1] \ldots \times [m_k]`.

    The iterator return at each step a pair ``(p,i)`` which corresponds to the
    modification to perform to get the next element. More precisely, one has to
    apply the increment ``i`` at the position ``p``. By construction, the
    increment is either ``+1`` or ``-1``.

    This is algorithm H in [Knuth-TAOCP2A]_: loopless reflected mixed-radix Gry
    generation.

    INPUT:

    - m {list} a list or tuple of positive integers that correspond to the size
      of the sets in the product

    OUTPUT: A list of every possible combination.

    """
    # n is the length of the element (we ignore sets of size 1)
    n = k = 0

    new_m = []   # will be the set of upper bounds m_i different from 1
    mm = []      # index of each set (we skip sets of cardinality 1)
    for i in m:
        i = int(i)
        if i <= 0:
            raise ValueError("accept only positive integers")
        if i >= 1:
            new_m.append(i-1)
            mm.append(k)
            n += 1
        k += 1

    m = new_m
    f = list(range(n + 1))  # focus pointer
    o = [1] * n     # switch +1 or -1
    a = [0] * n     # current element of the product

    j = f[0]
    _l = [0 for i in range(len(m))]
    every_solution = [list(_l)]
    while j != n:
        f[0] = 0
        oo = o[j]
        a[j] += oo
        if a[j] == 0 or a[j] == m[j]:
            f[j] = f[j+1]
            f[j+1] = j+1
            o[j] = -oo

        # Get Solution
        _l[mm[j]] += oo
        every_solution.append(list(_l))

        j = f[0]
    return every_solution


if __name__ == "__main__":
    base = 3
    length = 2

    power_set = gcombo(base, length)
    print(power_set)
