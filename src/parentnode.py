from collections.abc import Mapping, Sequence

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: Sequence[HTMLNode], props:Mapping[str,str]|None=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("parent nodes must have tags")
        if self.children is None:
            raise ValueError("Parent nodes must have children")

        child_html = "".join([child.to_html() for child in self.children])
        return  f"<{self.tag}{' ' + self.props_to_html() if self.props else ""}>{child_html}</{self.tag}>"


    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, ParentNode):
            return NotImplemented
        return super().__eq__(other)

    def __repr__(self) -> str:
        return f"LeafNode({self.tag=},{self.value=},{self.props=})"
