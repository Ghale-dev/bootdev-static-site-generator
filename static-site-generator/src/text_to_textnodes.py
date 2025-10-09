import unittest
from enum import Enum
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

# Import your existing classes and functions
# Adjust these import statements based on your actual file names
from your_previous_file import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link

# Main function
def text_to_textnodes(text):
    # Start with a single TEXT node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in order
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes

# Tests
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
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
        self.assertListEqual(nodes, expected)
    
    def test_text_to_textnodes_plain(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertListEqual(nodes, expected)
    
    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()
