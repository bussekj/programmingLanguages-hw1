from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):

    # initializes the empty dictionary
    def __init__(self, env):
        self.env: Dict[str, Optional[Any]] = {}

    # returns the item of the given key
    def __getitem__(self, key: str) -> Optional[Any]:
        return self.env[key]
    
    # stores an item at the given key
    def __setitem__(self, key: str, value: Optional[Any]) -> None:
        self.env[key] = value

    # deletes the item at the given key
    def __delitem__(self, key: str) -> None:
        del self.env[key]

    # returns an iterator over the keys of the dictionary
    def __iter__(self) -> Iterator[str]:
        return iter(self.env)
    
    # returns number of items in the dictionary
    def __len__(self) -> int:
        return len(self.env)

def get_dynamic_re() -> DynamicScope: 
    # sets stack and empty dictionary
    stack = inspect.stack()
    dictionary: Dict[str, Any] = {}

    # grabs the local variables in the stack frames
    for frameInfo in stack[1:]:
        # gets the frame and the local variables
        frame = frameInfo.frame
        localDictionary = frame.f_locals

        # filters the free variables
        freeVariables = set(frame.f_code.co_freevars)

        # iterates through the local variables in each frame
        for key, value in frame.f_locals.items():
            if key not in dictionary and key not in freeVariables:
                dictionary[key] = value


    return DynamicScope(dictionary)
