import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        case = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode(props=case)
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_props_to_html_2(self):
        case = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode("foo", "foofoo", "foofoofoo", case)
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_props_to_html_2(self):
        case = {
            "tag": "blue",
        }
        node = HTMLNode("foo", "foofoo", "foofoofoo", case)
        result = ' tag="blue"'
        self.assertEqual(node.props_to_html(), result)
    

if __name__ == "__main__":
    unittest.main()