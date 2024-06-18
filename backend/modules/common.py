from functools import reduce
from collections import deque
from typing import Callable, Iterator, Deque

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


def consume(i: Iterator) -> Deque:
    """
    Calls a lazy object to completion. Typically this is done to trigger side-effects.
    """
    return deque(i, maxlen=0)


def compose(*funcs: Callable) -> Callable:
    """
    Combines functions in left associative order.
    """
    def _compose2[a, b, c](x: Callable[[a], b], y: Callable[[b], c]) -> Callable[[a], c]:
        return lambda _: y(x(_))

    return reduce(_compose2,funcs)


def join_to_comma(i: Iterator[str]) -> str:
    """ """
    return ", ".join(list(i))


#
#
# TESTS
#
#
if __name__ == "__main__":
    assert(compose(len, lambda x: x + 10, lambda y: y - 1)("number should be 28") == 28)
