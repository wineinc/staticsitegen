
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from copy import deepcopy


class HTMLNode(ABC):
    def __init__(self, tag: str|None=None, value: str|None=None, children: Sequence["HTMLNode"]|None=None, props:Mapping[str,str]|None=None):
        self.tag = tag
        self.value = value
        self.children = deepcopy(children) if children is not None else None
        self.props = deepcopy(props) if props is not None else None

    @abstractmethod
    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props:
            ret:list[str] = []
            for prop, prop_value in self.props.items():
                ret.append(f'{prop}="{prop_value}"')
            return str.join(" ", ret)
        else:
            return ""

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented

        return (self.tag == other.tag and
            self.value == other.value and self.children == other.children and
            self.props == other.props)


    def __repr__(self) -> str:
        return f"HTMLNode({self.tag=},{self.value=},{self.children=},{self.props=})"
