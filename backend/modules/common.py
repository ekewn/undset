from collections import deque
from typing import Iterator, Deque

#
#
# TYPES
#
#


type IO = None

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
