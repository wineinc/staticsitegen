

import argparse
from pathlib import Path

from copystatic import copy_dir_tree
from generate_page import generate_page_recursive

dir_path_static = "./static"

## Update your main.py to build the site into the docs directory
## instead of public. GitHub pages serves sites from the docs directory of
## your main branch by default.
#dir_path_public = "./public"
dir_path_public = "./docs"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("app_root_dir", default="/")
    cmd_line_parsed = vars(parser.parse_args())
    print(f'{cmd_line_parsed["app_root_dir"]=}')
    base_path = cmd_line_parsed["app_root_dir"]
    print(f"Copying static files to {dir_path_public} directory...")
    print(f"{base_path=}")
    copy_dir_tree(dir_path_static, dir_path_public)


    generate_page_recursive(base_path, dir_path_content = Path("./content"), template_path = Path("./template.html"), dest_dir_path = Path(dir_path_public))



if __name__ == '__main__':
    main()
