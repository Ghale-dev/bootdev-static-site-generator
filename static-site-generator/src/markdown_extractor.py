import re
import unittest

def extract_markdown_images(text):
    # Pattern: ![alt text](url)
    pattern = r"!\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # Pattern: [anchor text](url)
    # Need to make sure we don't match images (which start with !)
    pattern = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)
    
    def test_extract_markdown_links_single(self):
        text = "Check out [this link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this link", "https://example.com")], matches)
    
    def test_no_images(self):
        text = "This is just plain text"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_no_links(self):
        text = "This is just plain text"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_mixed_images_and_links(self):
        text = "Here's a ![picture](https://example.com/pic.png) and a [link](https://example.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("picture", "https://example.com/pic.png")], images)
        self.assertListEqual([("link", "https://example.com")], links)

if __name__ == "__main__":
    # Demo the functions
    print("=== Demo ===")
    text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print("Images:", extract_markdown_images(text1))
    
    text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print("Links:", extract_markdown_links(text2))
    
    print("\n=== Running Tests ===")
    unittest.main()

if __name__ == "__main__":
    print(extract_markdown_images("A ![pic](url) B"))
