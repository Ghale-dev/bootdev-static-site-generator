from enum import Enum
from htmlnode import LeafNode
#Don’t import converter.py

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(tn: "TextNode") -> LeafNode:
    if tn.text_type == TextType.TEXT:
        return LeafNode(None, tn.text)
    if tn.text_type == TextType.BOLD:
        return LeafNode("b", tn.text)
    if tn.text_type == TextType.ITALIC:
        return LeafNode("i", tn.text)
    if tn.text_type == TextType.CODE:
        return LeafNode("code", tn.text)
    if tn.text_type == TextType.LINK:
        return LeafNode("a", tn.text, {"href": tn.url})
    if tn.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": tn.url, "alt": tn.text})
    raise ValueError(f"Unknown TextType: {tn.text_type}")
