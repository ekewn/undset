from collections import deque
from functools import partial, reduce
from itertools import accumulate, count, islice, repeat
from operator import add, contains, itemgetter
from typing import Callable, Dict, Iterable, Iterator, List

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


def mapc[a, b](f: Callable[[a], b]) -> Callable[[Iterable[a]], Iterable[b]]:
    """
    Curried map.
    """
    return partial(map, f)


def filterc[a](p: Callable[[a], bool]) -> Callable[[Iterable[a]], Iterable[a]]:
    """
    Curried filter.
    """
    return partial(filter, p)


def consume(i: Iterator) -> None:
    """
    Consumes an iterable to trigger side effects (avoids wasting the creation of a list).
    """
    deque(i, maxlen=0)


def compose(*funcs: Callable) -> Callable:
    """
    Composes functions from left to right.
    """
    def compose2[a, b, c](x: Callable[[a], b], y: Callable[[b], c]) -> Callable[[a], c]:
        return lambda val: y(x(val))

    return reduce(compose2, funcs)


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


def cond[a, b](predicate: bool, t: Callable[[], a], f: Callable[[], b]) -> a | b:
    """
    Functional ternary operator.
    """
    return t() if predicate else f()


def id[a](x: a) -> a:
    """
    The identity property. Returns the argument.
    """
    return x


def tap[a](f: Callable, x: a) -> a:
    """
    Calls a function and then returns the argument.
    """
    return compose(f, id)(x)


def get[a, b](d: Dict[a, b], default: b, key: a) -> b:
    return cond(contains(d, key)
                , partial(itemgetter(key), d)
                , partial(id, default))


#
#
# TESTS
#
#


if __name__ == "__main__":
    assert compose(len, lambda x: x + 10, lambda y: y - 1)("number should be 28") == 28
    assert take(4, iterate(partial(add, 3),2)) == [2, 5, 8, 11]
    assert take(3, drop(2, count())) == [2, 3, 4]
    assert cond(True, lambda: "a", lambda: "b") == "a"
    assert cond(False, lambda: "a", lambda: "b") == "b"
    assert id("1") == "1"
    assert tap(id, "2") == "2"
    assert get({"a" : 1, "b" : 2}, "defaultvalue", "a") == 1
    assert get({"a" : 1, "b" : 2}, "defaultvalue", "c") == "defaultvalue"


