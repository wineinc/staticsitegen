import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        props_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(props_node.to_html(),'<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "This is raw text without a tag.")
        self.assertEqual(node.to_html(), "This is raw text without a tag.")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "input",
            "",
            {"type": "text", "placeholder": "Enter name"}
        )
        self.assertEqual(
            node.to_html(),
            '<input type="text" placeholder="Enter name"></input>'
        )
