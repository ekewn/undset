from collections import deque
from functools import partial, reduce
from itertools import accumulate, count, islice, repeat
from operator import add
from typing import Any, Callable, Deque, Iterator, List

#
#
# TYPES
#
#


type IO       = None
type Fn[a, b] = Callable[[a], b]

#
#
# FUNCTIONS
#
#


def consume(i: Iterator) -> None: deque(i, maxlen=0)


def compose(*funcs: Callable) -> Callable:
    def _compose2[a, b, c](x: Callable[[a], b], y: Callable[[b], c]) -> Callable[[a], c]:
        return lambda _: y(x(_))

    return reduce(_compose2, funcs)


def take[a](n: int, i: Iterator[a]) -> List[a]: return list(islice(i, n))


def drop[a](n: int, i: Iterator[a]) -> Iterator[a]: return islice(i, n, None)


def iterate[a, b](f: Callable[[a], b], x: a) -> Iterator[b]:
    return accumulate(repeat(x), lambda fx, _ : f(fx)) #type: ignore


def cond[a, b](predicate: Callable[[Any], bool], t: a, f: b) -> a | b:
    return t if predicate else f


def id[a](x: a) -> a:
    return x


def tap[a](f: Callable, x: a) -> a:
    f(x)
    return x

#
#
# TESTS
#
#


if __name__ == "__main__":
    assert compose(len, lambda x: x + 10, lambda y: y - 1)("number should be 28") == 28
    assert take(4, iterate(partial(add, 3),2)) == [2, 5, 8, 11]
    assert take(3, drop(2, count())) == [2, 3, 4]

