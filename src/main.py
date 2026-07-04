

from pathlib import Path

from copystatic import copy_dir_tree
from generate_page import generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main() -> None:
    print("Copying static files to public directory...")
    copy_dir_tree(dir_path_static, dir_path_public)

#(dir_path_content: Path, template_path: Path, dest_dir_path: Path)
    generate_page_recursive(dir_path_content = Path("./content"), template_path = Path("./template.html"), dest_dir_path = Path(dir_path_public))



if __name__ == '__main__':
    main()
