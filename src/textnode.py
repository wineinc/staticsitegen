from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type:TextType, url:str|None = None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TextNode):
            return NotImplemented

        return (self.text_type == value.text_type and
            self.text == value.text and self.url == value.url)

    def __repr__(self) -> str:
        return f"TextNode({self.text=}, {self.text_type.value=}, {self.url=})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url, "target": "_blank", "rel" : "noopener"})
        case TextType.IMAGE:
            return LeafNode(tag="img", value = text_node.text, props={"alt": text_node.text, "src" : text_node.url})
        case _:
            raise ValueError(f"Unknown TextType={text_node.text_type.value}")
