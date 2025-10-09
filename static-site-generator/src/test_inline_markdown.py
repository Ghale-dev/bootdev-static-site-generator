import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_no_delimiter_returns_same_node(self):
        node_in = TextNode("hello world", TextType.TEXT)
        nodes_out = split_nodes_delimiter([node_in], "`", TextType.CODE)
        self.assertEqual(len(nodes_out), 1)
        self.assertEqual(nodes_out[0].text, "hello world")
        self.assertEqual(nodes_out[0].text_type, TextType.TEXT)

    def test_backtick_single_section_splits_into_three(self):
        node_in = TextNode("alpha `beta` gamma", TextType.TEXT)
        nodes_out = split_nodes_delimiter([node_in], "`", TextType.CODE)

        self.assertEqual(len(nodes_out), 3)

        self.assertEqual(nodes_out[0].text, "alpha ")
        self.assertEqual(nodes_out[0].text_type, TextType.TEXT)

        self.assertEqual(nodes_out[1].text, "beta")
        self.assertEqual(nodes_out[1].text_type, TextType.CODE)

        self.assertEqual(nodes_out[2].text, " gamma")
        self.assertEqual(nodes_out[2].text_type, TextType.TEXT)


    def test_unmatched_backtick_raises(self):
        node_in = TextNode("hello `world", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node_in], "`", TextType.TEXT)

    def test_unmatched_underscore_raises(self):
        node_in = TextNode("hello _world", TextType.ITALIC)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node_in], "_", TextType.ITALIC)

    def test_unmatched_asterisk_pair_raises(self):
        node_in = TextNode("hello **world", TextType.BOLD)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node_in], "**", TextType.BOLD)

    def test_backtick_two_sections_splits_into_five(self):
        node_in = TextNode("a `b` c `d` e", TextType.TEXT)
        nodes_out = split_nodes_delimiter([node_in], "`", TextType.CODE)
        self.assertEqual(len(nodes_out), 5)
        self.assertEqual(nodes_out[0].text, "a ")
        self.assertEqual(nodes_out[0].text_type, TextType.TEXT)
        self.assertEqual(nodes_out[1].text, "b")
        self.assertEqual(nodes_out[1].text_type, TextType.CODE)
        self.assertEqual(nodes_out[2].text, " c ")
        self.assertEqual(nodes_out[2].text_type, TextType.TEXT)
        self.assertEqual(nodes_out[3].text, "d")
        self.assertEqual(nodes_out[3].text_type, TextType.CODE)
        self.assertEqual(nodes_out[4].text, " e")
        self.assertEqual(nodes_out[4].text_type, TextType.TEXT)

    def test_code_single_section(self):
        n = TextNode("a `b` c", TextType.TEXT)
        out = split_nodes_delimiter([n], "`", TextType.CODE)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[1].text, "b")
        self.assertEqual(out[1].text_type, TextType.CODE)

    def test_italic_single_section(self):
        n = TextNode("a _b_ c", TextType.TEXT)
        out = split_nodes_delimiter([n], "_", TextType.ITALIC)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[1].text, "b")
        self.assertEqual(out[1].text_type, TextType.ITALIC)

    def test_bold_single_section(self):
        n = TextNode("a **b** c", TextType.TEXT)
        out = split_nodes_delimiter([n], "**", TextType.BOLD)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[1].text, "b")
        self.assertEqual(out[1].text_type, TextType.BOLD)

    def test_non_text_nodes_passthrough(self):
        link = TextNode("x", TextType.LINK)
        txt = TextNode("a `b` c", TextType.TEXT)
        out = split_nodes_delimiter([link, txt], "`", TextType.CODE)
        self.assertEqual(out[0].text, "x")
        self.assertEqual(out[0].text_type, TextType.LINK)
        self.assertEqual(len(out), 4)


if __name__ == "__main__":
    unittest.main()
