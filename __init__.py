from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):

    # initialize with an optional env dict (copy to avoid aliasing)
    def __init__(self, env: Optional[Dict[str, Any]] = None):
        self.env: Dict[str, Optional[Any]] = dict(env) if env is not None else {}

    # returns the item of the given key
    def __getitem__(self, key: str) -> Optional[Any]:
        if key not in self.env:
            raise NameError(f"Name '{key}' not found.")
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
    env: Dict[str, Any] = {}

    # grabs the local variables in the stack frames
    for frame_info in stack[1:]:
        # gets the frame and the local variables
        frame = frame_info.frame
        localDictionary = frame.f_locals

        # filters the free variables
        freeVariables = set(frame.f_code.co_freevars)

        # iterates through the local variables in each frame
        for key, value in localDictionary.items():
            if key not in env and key not in freeVariables:
                env[key] = value


    return DynamicScope(env)
