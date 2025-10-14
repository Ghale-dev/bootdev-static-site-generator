import os
from gencontent import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"

def generate_page(from_path, template_path, dest_path, basepath="/"):
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()
    title = extract_title(md)
    html = markdown_to_html_node(md).to_html()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        print(f"Writing: {dest_path}")
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    print(f"Scanning: {dir_path_content}")
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path) and full_path.endswith(".md"):
            rel = os.path.relpath(full_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, os.path.splitext(rel)[0] + ".html")
            print(f"MD: {full_path} -> {dest_path}")
            generate_page(full_path, template_path, dest_path, basepath=basepath)
        elif os.path.isdir(full_path):
            new_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(full_path, template_path, new_dest, basepath=basepath)
