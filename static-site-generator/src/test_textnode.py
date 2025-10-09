import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Goodbye", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_Text(self):
        node = TextNode("Link to Boot.dev", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Link to Boot.dev", TextType.LINK, "https://blog.boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
