from collections import deque
from functools import partial, reduce
from itertools import accumulate, count, islice, repeat
import operator as op
from operator import add, contains, is_not, itemgetter, methodcaller
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional

#
#
# DATA
#
#


type IO       = None
type Fn[a, b] = Callable[[a], b]
type IOFn[a, b] = Callable[[a], b]

#
#
# FUNCTIONS
#
#


# Curried Classics

def map_[a, b](fn: Callable[[a], b]) -> Callable[[Iterable[a]], Iterable[b]]:
    """
    Curried map.
    """
    return partial(map, fn)


def filter_[a](p: Callable[[a], bool]) -> Callable[[Iterable[a]], Iterable[a]]:
    """
    Curried filter.
    """
    return partial(filter, p)


# Composers

def compose(*funcs: Callable) -> Callable:
    """
    Composes functions from left to right.
    """
    def compose2[a, b, c](x: Callable[[a], b], y: Callable[[b], c]) -> Callable[[a], c]:
        return lambda val: y(x(val))

    return reduce(compose2, funcs)


# Composition Helpers

def if_else[a, b, c](p: Fn[a, bool], if_true: Fn[a, b], if_false: Fn[a , c]) -> Fn[a, b | c]:
    """
    Functional ternary operator.
    """
    return lambda x: if_true(x) if p(x) else if_false(x)


def id[a](x: a) -> a:
    """
    The identity property. Returns the argument.
    """
    return x


def tap[a](fn: Callable, x: a) -> a:
    """
    Calls a function and then returns the argument.
    """
    return compose(fn, id)(x)


def const[a](x: a, _: Any) -> Callable[[], a]:
    """
    Returns a nullary function that always returns the first argument, and ignores the second.
    """
    return partial(id, x)


# Logical

not_     = op.not_
and_     = op.and_
or_      = op.or_
contains = op.contains
is_      = op.is_
is_not   = op.is_not
truth    = op.truth


def both[a](p1: Fn[a, bool], p2: Fn[a, bool]) -> Fn[a, bool]:
    """
    Returns a function that returns True if both of the predicates are true.
    """
    return lambda x: and_(p1(x), p2(x))


def either[a](p1: Fn[a, bool], p2: Fn[a, bool]) -> Fn[a, bool]:
    """
    Returns a function that returns True if either of the predicates are true.
    """
    return lambda x: or_(p1(x), p2(x))


# Container-related

def default[a](val: a, fn: Fn[..., Optional[a]], *args) -> Fn[..., a]:
    return val if fn(args) is None else fn(args)


def empty[a: (List, Dict, int, str)](x: a) -> a:
    """
    Returns the empty value (identity) of the monoid.
    e.g. [], {}, "", or 0.
    """
    is_a = partial(isinstance, x)
    if is_a(List):
        return [] #type:ignore
    elif is_a(Dict):
        return {} #type:ignore
    elif is_a(int):
        return 0 #type:ignore
    else:
        return "" #type:ignore


def is_empty[a: (List, Dict, int, str)](x: a) -> bool:
    """
    Checks if value is the identity value of the monoid.
    """
    return any([x == [], x == {}, x == "", x == 0])


# Iterator Specifics

def consume(i: Iterator) -> None:
    """
    Consumes an iterable to trigger side effects (avoids wasting the creation of a list).
    """
    deque(i, maxlen=0)


def take[a](n: int, i: Iterator[a]) -> List[a]:
    """
    Takes the first n from an iterator.
    """
    return list(islice(i, n))


def drop[a](n: int, i: Iterator[a]) -> Iterator[a]: 
    """
    Drops the first n from an iterator.
    """
    return islice(i, n, None)


def iterate[a](f: Callable[[a], a], x: a) -> Iterator[a]:
    """
    Creates an iterator by applying the same function to the result of f(x).
    """
    return accumulate(repeat(x), lambda fx, _ : f(fx))


# List Functions

find_first = op.indexOf


def adjust[a](idx: int, fn:Fn[a, a], l: List[a]) -> List[a]:
    """
    Returns a copy of the given list with the element at the index transformed by the given function. The original list remains unchanged.
    """
    l2 = l.copy()
    l2[idx] = fn(l2[idx])
    return l2


def head[a](i: List[a]) -> a:
    """
    Gets first item from a list without mutating.
    """
    return itemgetter(0)(i)


# Dictionary Functions

def get[a, b](d: Dict[a, b], default: b, key: a) -> b:
    return methodcaller("get", key, default)(d)


#
#
# TESTS
#
#


if __name__ == "__main__":
    assert compose(len, lambda x: x + 10, lambda y: y - 1)("number should be 28") == 28
    assert take(4, iterate(partial(add, 3),2)) == [2, 5, 8, 11]
    assert take(3, drop(2, count())) == [2, 3, 4]
    assert if_else(, lambda: "a", lambda: "b") == "a"
    assert if_else(False, lambda: "a", lambda: "b") == "b"
    assert id("1") == "1"
    assert tap(id, "2") == "2"
    assert get({"a" : 1, "b" : 2}, "defaultvalue", "a") == 1
    assert get({"a" : 1, "b" : 2}, "defaultvalue", "c") == "defaultvalue"


