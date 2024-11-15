import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "foo.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "bar.com")
        self.assertNotEqual(node, node2)
    
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.CODE, url = None)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)
        
    def test_eq4(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()