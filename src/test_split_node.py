import unittest

from split_node import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)
from textnode import TextNode, TextType


class Test_split_nodes_delimiter(unittest.TestCase):

    def test_unclosed_delimiter(self):
        node = TextNode("This is text with an unclosed `code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_CodeNode_interior(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #print(f"\ntest_CodeNode_interior: {new_nodes=}\n")
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_CodeNode_front(self):
        node = TextNode("`This is text with a `code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #print(f"\ntest_CodeNode_front: {new_nodes=}\n")
        expected = [
            TextNode("This is text with a ", TextType.CODE),
            TextNode("code block word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_CodeNode_back(self):
        node = TextNode("This is text with a code block `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a code block ", TextType.TEXT),
            TextNode("word", TextType.CODE),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_CodeNode_multiple(self):
        node = TextNode("`This` is text with a `code block` `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #print(f"\ntest_CodeNode_multiple: {new_nodes=}\n")
        expected = [
            TextNode("This", TextType.CODE),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("word", TextType.CODE),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_BoldNode(self):
        node = TextNode("This is **text** with a `code block` `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        #print(f"\ntest_CodeNode_multiple: {new_nodes=}\n")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a `code block` `word`", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_extract_markdown_images_positive(self):
        raw_text = r"This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        #print(extract_markdown_images(raw_text))
        expected = [("rick roll", r"https://i.imgur.com/aKaOqIh.gif"), ("obi wan", r"https://i.imgur.com/fJRm4Vk.jpeg")]
        actual = extract_markdown_images(raw_text)
        self.assertListEqual(actual, expected)

    def test_extract_markdown_images_negative(self):
        raw_text = r"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        #print(extract_markdown_images(raw_text))
        expected = []
        actual = extract_markdown_images(raw_text)
        self.assertListEqual(actual, expected)

    def test_extract_markdown_links_positive(self):
        raw_text = r"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        #print(extract_markdown_links(raw_text))
        expected= [("to boot dev", r"https://www.boot.dev"), ("to youtube", r"https://www.youtube.com/@bootdotdev")]
        actual = extract_markdown_links(raw_text)
        self.assertListEqual(actual, expected)

    def test_extract_markdown_links_negative(self):
        raw_text = r"This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        #print(extract_markdown_links(raw_text))
        expected = []
        actual = extract_markdown_links(raw_text)
        self.assertListEqual(actual, expected)

    def test_image_with_no_text(self):
        raw_text = r"An empty image: ![](https://boot.dev/logo.png)"
        expected = [("", "https://boot.dev/logo.png")]
        actual = extract_markdown_images(raw_text)
        #print(f"{actual=}")
        self.assertListEqual(actual, expected)

    def test_link_with_no_text(self):
        raw_text = r"This is no text with a link [](https://www.boot.dev)"
        expected = [("", "https://www.boot.dev")]
        actual = extract_markdown_links(raw_text)
        #print(f"{actual=}")
        self.assertListEqual(actual, expected)

    def test_link_with_no_links(self):
        raw_text = r"This is no text with a no links"
        expected = []
        actual = extract_markdown_links(raw_text)
        #print(f"{actual=}")
        self.assertListEqual(actual, expected)

    def test_link_with_no_images(self):
        raw_text = r"This is no text with a no images"
        expected = []
        actual = extract_markdown_images(raw_text)
        #print(f"test_link_with_no_images: {actual=}")
        self.assertListEqual(actual, expected)


    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        #print(f"\ntest_split_nodes_images: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_images_front(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) |This is text with an |and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        #print(f"\ntest_split_images_front: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" |This is text with an |and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_images_interior(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and nothing else",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        #print(f"\ntest_split_images_front: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing else", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_images_no_image(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        #print(f"\ntest_split_images_no_image: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        #print(f"\ntest_split_nodes_links: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_links_front(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) |This is text with an |and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        #print(f"\ntest_split_links_front: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" |This is text with an |and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_links_interior(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and nothing else",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        #print(f"\ntest_split_links_front: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing else", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_links_no_link(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        #print(f"\ntest_split_links_no_link: {new_nodes=}")
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_duplicate_image(self):
        node = TextNode(
            "![cat](https://cat.png) and then again ![cat](https://cat.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://cat.png"),
                TextNode(" and then again ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://cat.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_non_text_node_passthrough(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("bold text", TextType.BOLD)], new_nodes)

    def test_split_nodes_image_mixed_list(self):
        nodes = [
            TextNode("![cat](https://cat.png)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://cat.png"),
                TextNode("already bold", TextType.BOLD),
                TextNode("plain text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_only(self):
        node = TextNode("![cat](https://cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("cat", TextType.IMAGE, "https://cat.png")],
            new_nodes,
        )

    def test_split_nodes_link_ignores_images(self):
        node = TextNode(
            "![image](https://img.png) and [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![image](https://img.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes(self):
        text  = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        actual = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(actual, expected)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        #print(f"\n{md=}\n")
        #print(f"\n{blocks=}\n")
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        #print(f"\n{expected=}\n")
        self.assertEqual(
                blocks,
                expected
            )
