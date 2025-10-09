import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_none_returns_empty(self):
        node = HTMLNode("a", "link", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_empty_returns_empty(self):
        node = HTMLNode("a", "link", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_multiple_attributes(self):
        node = HTMLNode("a", "link", None, {"href": "https://x.com", "target": "_blank"})
        out = node.props_to_html()
        self.assertIn(' href="https://x.com"', out)
        self.assertIn(' target="_blank"', out)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_LeafNode_empty_returns_empty(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None, None)
            node.to_html()

    def test_leafnode_no_tag_returns_value(self):
        leaf_node = LeafNode(None, "This is raw text.")
        actual_output = leaf_node.to_html()
        expected_output = "This is raw text."
        self.assertEqual(actual_output, expected_output)

    def test_leafnode_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        actual_html = node.to_html()
        self.assertEqual(actual_html, '<a href="https://www.google.com">Click me!</a>')

    def test_parent_with_leaf_child(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        assert parent.to_html() == "<div><span>child</span></div>"

if __name__ == "__main__":
    unittest.main()
