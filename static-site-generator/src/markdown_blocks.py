import unittest

def markdown_to_blocks(markdown):
    # Split on double newlines
    blocks = markdown.split("\n\n")
    
    # Strip whitespace and filter out empty blocks
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            filtered_blocks.append(stripped_block)
    
    return filtered_blocks


def block_to_block_type(block: str):
    lines = block.split("\n")

    #code block
    non_empty = [ln.strip() for ln in lines if ln.strip() != ""]
    if non_empty and non_empty[0] == "```" and non_empty[-1] == "```":
        return "code"

    #heading
    first_line = block.split("\n")[0].lstrip()
    hashes = 0
    for ch in first_line:
        if ch == "#" and hashes < 6:
            hashes += 1
        else:
            break
    if 1 <= hashes <= 6 and len(first_line) > hashes and first_line[hashes] == " ":
        return "heading"

    # quote
    nonblank = [ln for ln in lines if ln.strip() != ""]
    if nonblank and all(ln.startswith("> ") for ln in nonblank):
        return "quote"

    # unordered list
    bullets = ("- ", "* ", "+ ")
    if nonblank and all(any(ln.startswith(b) for b in bullets) for ln in nonblank):
        return "unordered_list"

    # ordered list
    def is_ordered(ln: str) -> bool:
        i = 0
        while i < len(ln) and ln[i].isdigit():
            i += 1
        return i > 0 and i + 1 <= len(ln) and ln[i:i+2] == ". "
    if nonblank and all(is_ordered(ln) for ln in nonblank):
        return "ordered_list"

    return "paragraph"

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
First block


Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])
    
    def test_markdown_to_blocks_single_block(self):
        md = "Just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block"])
    
    def test_markdown_to_blocks_with_spacing(self):
        md = "   Block with spaces   \n\n\n   Another block   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with spaces", "Another block"])
    
    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

if __name__ == "__main__":
    unittest.main()
    from pprint import pprint
    sample = "## Hello\n\nParagraph"
    pprint(markdown_to_blocks(sample))
