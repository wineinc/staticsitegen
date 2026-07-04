from __future__ import annotations

from collections.abc import Mapping

from htmlnode import HTMLNode



class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str, props:Mapping[str,str]|None=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")

        if self.tag is not None:
            return  f"<{self.tag}{' ' + self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>"
        else:
            return  self.value

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, LeafNode):
            return NotImplemented
        return super().__eq__(other)

    def __repr__(self) -> str:
        return f"LeafNode({self.tag=},{self.value=},{self.props=})"


