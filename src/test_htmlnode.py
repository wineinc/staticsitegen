import unittest
from collections.abc import Mapping, Sequence

from htmlnode import HTMLNode


class TestingHTMLNode(HTMLNode):
    def __init__(self, tag: str|None=None, value: str|None=None, children: Sequence["HTMLNode"]|None=None, props:Mapping[str,str]|None=None):
        super().__init__(tag, value, children, props)

    def to_html(self) -> str:
        return ""

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = TestingHTMLNode("b")
        node2 = TestingHTMLNode("b")

        self.assertEqual(node, node2)

        node2 = TestingHTMLNode("p")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        propNode = TestingHTMLNode("span", props={
            "href": "https://www.google.com",
            "target": "_blank",
        }  )
        self.assertEqual(propNode.props_to_html(), 'href="https://www.google.com" target="_blank"')

        propNode = TestingHTMLNode("span", props=None)
        self.assertEqual(propNode.props_to_html(), '')

        propNode = TestingHTMLNode("span", props={})
        self.assertEqual(propNode.props_to_html(), '')




if __name__ == "__main__":
    unittest.main()
