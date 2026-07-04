from collections import deque
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")

class UniqueSequence(Generic[T]):
    """A container that maintains uniqueness and order."""
    def __init__(self, initial: Iterable[T] = None):
        self._set = set()
        self._queue = deque()
        if initial:
            for item in initial:
                self.add(item)

    def add(self, item: T):
        if item not in self._set:
            self._set.add(item)
            self._queue.append(item)

    def append(self, item:T):
        return self.add(item)

    def pop_next(self) -> T:
        item = self._queue.popleft()
        # Note: We keep it in the set so 'add' still enforces uniqueness
        return item

    def popleft(self) -> T:
        return self.pop_next()

    def popright(self) -> T:
        return self._queue.pop()

    def __contains__(self, item: T) -> bool:
        return item in self._set

    def __len__(self) -> int:
        return len(self._queue)

    def to_list(self) -> list[T]:
        # For extracting the final 'order'
        return list(self._queue)
