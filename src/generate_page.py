

from functools import reduce
from os import walk
from pathlib import Path

import blocktype as bt


def generate_page(base_path: Path, from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    md = from_path.read_text()
    template = template_path.read_text()

    title = bt.extract_title(md)
    html = bt.markdown_to_html_node(md).to_html()

    page_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    print("=" * 20)
    print(dest_path)
    print(f"{base_path=}")

    page_html_base = page_html.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    if page_html_base != page_html:
        print(f"page_html_base contains href={base_path} : {f'href="{base_path}' in page_html_base}")
        print(f"page_html_base contains src={base_path} : {f'src="{base_path}' in page_html_base}")

    else:
        print("substituting in base_path had no effect")

    if str(dest_path) == "/docs/index.html":
        print(page_html)
        print("--" * 6)
        print(page_html_base)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(page_html_base)



def generate_page_recursive(base_path: Path, dir_path_content: Path, template_path: Path, dest_dir_path: Path) -> None:
    for dir_path_str, dir_names, file_names in walk(dir_path_content):
        dir_path = Path(dir_path_str)
        for md_file_path in [Path(f) for f in file_names if f.endswith(".md")]:
            relative_dir = dir_path.relative_to(dir_path_content)
            dest_path_name = dest_dir_path / relative_dir / (md_file_path.stem + ".html")
            generate_page(base_path, from_path=dir_path / md_file_path, template_path=template_path, dest_path=dest_path_name)
