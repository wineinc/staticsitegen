import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, "fake url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        obj = object()
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
        node = TextNode("This is a image node", TextType.LINK, url="www.google.com")
        html_node = text_node_to_html_node(node)
        #print(html_node.to_html())
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props["href"], node.url)

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, url="www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props["alt"], node.text)
        self.assertEqual(html_node.props["src"], node.url)

if __name__ == "__main__":
    unittest.main()
