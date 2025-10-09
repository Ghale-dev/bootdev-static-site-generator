
from src.main import markdown_to_html_node

md = """
# Title

This is **bolded** paragraph
text in a p
tag here

- one
- two
- three

> quoted text

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

print(markdown_to_html_node(md).to_html())
