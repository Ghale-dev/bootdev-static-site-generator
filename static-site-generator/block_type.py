import unittest
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    
    # Check for heading (starts with 1-6 # followed by space)
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with 1. 2. 3. etc.)
    if lines[0].startswith("1. "):
        is_ordered = True
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_h2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_no_space(self):
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_too_many_hashes(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        block = "```\ncode here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_no_closing(self):
        block = "```\ncode here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multi_line(self):
        block = ">First line\n>Second line\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_incomplete(self):
        block = ">First line\nNot a quote\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_single_item(self):
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_no_space(self):
        block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_single_item(self):
        block = "1. Single item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_wrong_start(self):
        block = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_wrong_order(self):
        block = "1. First\n3. Third\n2. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_no_space(self):
        block = "1.First\n2.Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_plain(self):
        block = "This is just a regular paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multi_line(self):
        block = "This is a paragraph\nwith multiple lines\nthat don't match any pattern"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
