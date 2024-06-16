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


def join_to_comma(i: Iterator[str]) -> str:
    """ """
    return ", ".join(list(i))
