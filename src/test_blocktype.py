import unittest

from blocktype import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class Test_block_to_block_type(unittest.TestCase):
    def test_heading_types_positive(self):
        md = "# heading 1"
        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.HEADING)


    def test_heading_types_negative(self):
        md = "not heading"
        actual = block_to_block_type(md)

        self.assertNotEqual(actual, BlockType.HEADING)

    def test_code_negative(self):
        md = "```\nCode\n``"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_code_positive(self):
        md = "```\nCode\n```"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.CODE)

    def test_quote_positive(self):
        md = ">Quote line 1\n>Quote line 2"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.QUOTE)

    def test_quote_negative(self):
        md = ">Quote line 1\nQuote line 2\n>Quote line 3"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_unordered_list_positive(self):
        md = "- UL line 1\n- UL line 2"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.UNORDERED_LIST)

    def test_unordered_list_negative(self):
        md = "- UL line 1\nUL line 2\n- UL line 3"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_ordered_list_positive(self):
        md = "1. UL line 1\n2. UL line 2\n3. UL line 3"

        actual = block_to_block_type(md)
        #print(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.ORDERED_LIST)

    def test_ordered_list_negative(self):
        md = "1. UL line 1\n3. UL line 2\n3. UL line 3"

        actual = block_to_block_type(md)
        #print(f"{actual=}")
        self.assertEqual(actual, BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        md = "just a normal paragraph"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_heading_requires_space(self):
        md = "#heading"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_quote_allows_no_space_after_gt(self):
        md = ">line 1\n>line 2"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_ordered_list_must_start_at_1(self):
        md = "2. item\n3. item"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title_positive(self):
        md = "# Hello, I am #7\n\n"
        md += "## This is a sub-heading"
        actual = extract_title(md)
        #print(f"{actual=}")
        self.assertEqual(actual,"Hello, I am #7")

    def test_extract_title_negative(self):
        md = "# \n\n"

        with self.assertRaises(Exception):
            actual = extract_title(md)
            #print(f"{actual=}")


    def test_extract_title_negative_2(self):
        md = "\n"
        md += "## This is a sub-heading"

        with self.assertRaises(Exception):
            actual = extract_title(md)
            #print(f"{actual=}")

if __name__ == "__main__":
    unittest.main()
