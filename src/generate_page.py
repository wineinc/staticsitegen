

from functools import reduce
from os import walk
from pathlib import Path

import blocktype as bt


def generate_page_v1(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    md = ""
    with open(from_path, "r") as md_stream:
        md = md_stream.read()

    with open(template_path, "r") as template_stream:
        template = template_stream.read()

    title = bt.extract_title(md)
    html = bt.markdown_to_html_node(md).to_html()

    page_html = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html)

    with open(dest_path, "w") as output_html:
        output_html.write(page_html)




def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    md = from_path.read_text()
    template = template_path.read_text()

    title = bt.extract_title(md)
    html = bt.markdown_to_html_node(md).to_html()

    page_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(page_html)


def generate_page_recursive_v1(dir_path_content: Path, template_path: Path, dest_dir_path: Path) -> None:

    for dir_path, dir_names, file_names in walk(dir_path_content):
        if "index.md" in file_names:
            dir_path = Path(dir_path)
            dest_path_name = Path("public/" + reduce(lambda s, p: s+"/"+p,dir_path.parts[1:],"") + "/index.html")
            #print(f"{dir_path=}\n{dir_path_content=}\n{dest_dir_path=}\n{dir_path.parts[1:]=}\n{dest_path_name=}")
            generate_page(from_path=dir_path / "index.md", template_path=Path(template_path), dest_path=dest_path_name)


def generate_page_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path) -> None:
    for dir_path_str, dir_names, file_names in walk(dir_path_content):
        dir_path = Path(dir_path_str)
        for md_file_path in [Path(f) for f in file_names if f.endswith(".md")]:    
            relative_dir = dir_path.relative_to(dir_path_content)
            dest_path_name = dest_dir_path / relative_dir / (md_file_path.stem + ".html")
            generate_page(from_path=dir_path / md_file_path, template_path=template_path, dest_path=dest_path_name)
