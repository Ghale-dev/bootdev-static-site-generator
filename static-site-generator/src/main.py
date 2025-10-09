from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from markdown_blocks import markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from copystatic import copy_static

def inline_children_from_text(text: str):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

def paragraph_node(block: str):
    # collapse internal newlines to spaces for paragraphs
    text = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", inline_children_from_text(text))

def codeblock_node(block: str):
    lines = block.split("\n")
    # remove surrounding ``` lines, keep inner text with original newlines
    inner = "\n".join(lines[1:-1]) + ("\n" if block.endswith("\n```") else "")
    code_leaf = LeafNode("code", inner)
    return ParentNode("pre", [code_leaf])

def heading_node(block: str):
    first = block.split("\n")[0].lstrip()
    level = 0
    for ch in first:
        if ch == "#" and level < 6:
            level += 1
        else:
            break
    # remove leading hashes + space
    text = first[level+1:]
    return ParentNode(f"h{level}", inline_children_from_text(text))

def quote_node(block: str):
    lines = [ln[2:] if ln.startswith("> ") else ln for ln in block.split("\n")]
    text = " ".join(ln.strip() for ln in lines)
    return ParentNode("blockquote", inline_children_from_text(text))

def ul_node(block: str):
    items = []
    for ln in block.split("\n"):
        if ln.strip() == "":
            continue
        if ln.startswith(("- ", "* ", "+ ")):
            content = ln[2:]
        else:
            content = ln
        items.append(ParentNode("li", inline_children_from_text(content)))
    return ParentNode("ul", items)

def ol_node(block: str):
    items = []
    for ln in block.split("\n"):
        if ln.strip() == "":
            continue
        i = 0
        while i < len(ln) and ln[i].isdigit():
            i += 1
        if i > 0 and ln[i:i+2] == ". ":
            content = ln[i+2:]
        else:
            content = ln
        items.append(ParentNode("li", inline_children_from_text(content)))
    return ParentNode("ol", items)

def markdown_to_html_node(markdown: str):
    children = []
    for block in markdown_to_blocks(markdown):
        btype = block_to_block_type(block)
        if btype == "heading":
            children.append(heading_node(block))
        elif btype == "code":
            children.append(codeblock_node(block))
        elif btype == "quote":
            children.append(quote_node(block))
        elif btype == "unordered_list":
            children.append(ul_node(block))
        elif btype == "ordered_list":
            children.append(ol_node(block))
        else:
            children.append(paragraph_node(block))
    return ParentNode("div", children)

def main():
    #node = TextNode("hi", TextType.TEXT)
    #print(node)
    copy_static("static", "public")

if __name__ == "__main__":
    main()
