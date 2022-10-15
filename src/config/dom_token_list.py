from typing import Any, Callable, Generic, Iterable, List, TypeVar


_T = TypeVar('_T')
CHANGE_CALLBACK = Callable[[List[_T]], None]


class DomTokenList(Generic[_T]):
    def __init__(self, change_callback: CHANGE_CALLBACK[_T], iterable: Iterable[_T]) -> None:
        self.__change_callback = change_callback
        self.__list = list(iterable)
    
    def __getitem__(self, index: int) -> _T:
        return self.__list[index]
    
    def __setitem__(self, index: int, value: _T) -> None:
        self.__list[index] = value
        self.__change_callback(self.__list)
    
    def __delitem__(self, index: int) -> None:
        del self.__list[index]
        self.__change_callback(self.__list)
    
    def __len__(self) -> int:
        return len(self.__list)
    
    def __iter__(self):
        return iter(self.__list)
    
    def __contains__(self, item: _T) -> bool:
        return item in self.__list
    
    def __reversed__(self):
        return reversed(self.__list)
    
    def __repr__(self) -> str:
        return repr(self.__list)
    
    def __str__(self) -> str:
        return str(self.__list)
    
    def append(self, item: _T) -> None:
        self.__list.append(item)
        self.__change_callback(self.__list)
    
    def clear(self) -> None:
        self.__list.clear()
        self.__change_callback(self.__list)
    
    def copy(self) -> 'DomTokenList[_T]':
        return DomTokenList(self.__change_callback, self.__list.copy())
    
    def count(self, item: _T) -> int:
        return self.__list.count(item)
    
    def extend(self, items: Iterable[_T]) -> None:
        self.__list.extend(items)
        self.__change_callback(self.__list)
    
    def index(self, item: _T, start: int = 0, stop: int = 0) -> int:
        return self.__list.index(item, start, stop)
    
    def insert(self, index: int, item: _T) -> None:
        self.__list.insert(index, item)
        self.__change_callback(self.__list)
    
    def pop(self, index: int = -1) -> _T:
        item = self.__list.pop(index)
        self.__change_callback(self.__list)
        return item
    
    def remove(self, item: _T) -> None:
        out = self.__list.remove(item)
        self.__change_callback(self.__list)
        return out
    
    def reverse(self) -> None:
        out = self.__list.reverse()
        self.__change_callback(self.__list)
        return out
    

if __name__ == "__main__":
    def change(*args: Iterable[Any]):
        print("changed", args)
    a = DomTokenList(change, [1, 2, 3])
    a.append(4)
    a.extend([5, 6])
    b = a.pop()
    print(b)
