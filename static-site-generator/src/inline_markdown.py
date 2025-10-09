from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images
from markdown_extractor import extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]
    for old_node in old_nodes:
        if old_node.text_type not in (TextType.TEXT, text_type):
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        split_nodes = []
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes            


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        while True:
            imgs = extract_markdown_images(text)
            if not imgs:
                break
            alt, url = imgs[0]
            token = f"![{alt}]({url})"
            before, after = text.split(token, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        while True:
            links = extract_markdown_links(text)
            if not links:
                break
            label, url = links[0]
            token = f"[{label}]({url})"
            before, after = text.split(token, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, url))
            text = after
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


if __name__ == "__main__":
    n = TextNode("A ![x](u) B", TextType.TEXT)
    print(split_nodes_image([n]))

