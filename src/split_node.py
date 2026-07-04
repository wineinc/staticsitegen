import re
from collections.abc import Sequence
from itertools import zip_longest

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: Sequence[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ret.append(old_node)
            continue
        segments = old_node.text.split(delimiter)

        if len(segments) % 2 == 0:
            raise ValueError("Invalid markdown syntax: unmatched delimiter")

        for i, segment in enumerate(segments):
            if segment == "":
                continue
            new_node_type = text_type if i % 2  == 1 else TextType.TEXT
            ret.append(TextNode(text=segment, text_type = new_node_type))
    return ret

def extract_markdown_images(raw_text: str) -> list[tuple[str,str]]:
    '''
    Takes raw markdown text and returns a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images.
    For example:
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    '''
    return re.findall(r"!\[([^\]]*)\]\(([^\)]+)\)", raw_text)

def extract_markdown_links(raw_text:str) -> list[tuple[str,str]]:
    '''
    extracts markdown links instead of images. It should return tuples of anchor text and URLs.
    For example:
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    '''
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]+)\)", raw_text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ret.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        not_images = re.split(r"!\[[^\]]*\]\([^\)]+\)", old_node.text)
        for not_image, image in zip_longest(not_images, images):
            if not_image:
                ret.append(TextNode(not_image,TextType.TEXT))
            if image:
                image_text, image_url = image
                ret.append(TextNode(image_text ,TextType.IMAGE, image_url))
    return ret

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
        ret = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                ret.append(old_node)
                continue
            links = extract_markdown_links(old_node.text)
            not_links = re.split(r"(?<!!)\[[^\]]*\]\([^\)]+\)", old_node.text)
            for not_link, link in zip_longest(not_links, links):
                if not_link:
                    ret.append(TextNode(not_link,TextType.TEXT))
                if link:
                    link_text, link_url = link
                    ret.append(TextNode(link_text ,TextType.LINK, link_url))
        return ret

def text_to_text_nodes(text:str) -> list[TextNode]:
    start = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([start], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown_document:str) -> list[str]:
    return [ stripped  for s in markdown_document.split("\n\n") if (stripped := s.strip())]
