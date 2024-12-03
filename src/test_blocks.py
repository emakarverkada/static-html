import unittest
from textnode import *
from markdown import *
from htmlnode import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_html(self):
        md = """```
This is a code paragraph
It takes code and does it
idk
```
"""
        block = markdown_to_blocks(md)
        self.assertEqual(
            block_to_html(block[0], BlockType.CODE),
            ParentNode("code", [
                LeafNode(tag = None, value = "This is a code paragraph"),
                LeafNode(tag = None, value = "It takes code and does it"),
                LeafNode(tag = None, value = "idk")
                ]
            )
        )

if __name__ == "__main__":
    unittest.main()
