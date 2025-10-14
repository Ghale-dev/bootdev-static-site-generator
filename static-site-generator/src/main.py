import os, sys, shutil
from copystatic import copy_static
from generate_page import generate_pages_recursive

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    static_dir = os.path.join(project_root, "static")
    output_dir = os.path.join(project_root, "docs")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    copy_static(static_dir, output_dir)

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive(content_dir, template_path, output_dir, basepath=basepath)

if __name__ == "__main__":
    main()
