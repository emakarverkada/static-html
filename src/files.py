import shutil
import os
from markdown import markdown_to_html_node, extract_title

def cp_directory(from_path, dest_path):
    print(f"Removing directory {dest_path}")
    shutil.rmtree(dest_path)
    print(f"Copying directory {from_path} to {dest_path}")
    shutil.copytree(from_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f: md = f.read()
    with open(template_path) as f: template = f.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    new_page = template.replace("{{ Title }}",title).replace("{{ Content }}", html)
    os.makedirs(dest_path, exist_ok=True)
    with open(dest_path, "w") as f: f.write(new_page)
