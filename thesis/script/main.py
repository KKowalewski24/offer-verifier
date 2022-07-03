import glob
import os
import pathlib
import shutil
import subprocess
import sys
import webbrowser
from argparse import ArgumentParser, Namespace
from typing import Callable, List

"""
* Building project `python main.py -r`
* Opening pdf file `python main.py -o`
* Cleaning project `python main.py -c`

* Building options 
    Check types - `python main.py -t`
    
"""

# VAR ------------------------------------------------------------------------ #
PDF_LATEX = "pdflatex"
BIBER = "biber"

TEX_FILENAME = "Kamil_Kowalewski_Main"
PDF = ".pdf"
TEX = ".tex"

SOURCE_DIRECTORY = "src"
DIRECTORIES = ["auxil", "out"]
FILE_EXTENSIONS = [
    "*.aux", "*.bcf", "*.locode", "*.lof", "*.log",
    "*.lot", "*.lot", "*.pdf", "*.out", "*.xml", "*.gz", "*.toc"
]


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    run: bool = args.run
    open_file: bool = args.open
    clean: bool = args.clean

    if run:
        build_project()
    elif open_file:
        open_generated_pdf()
    elif clean:
        clean_project()

    display_finish()


# DEF ------------------------------------------------------------------------ #
def build_project() -> None:
    go_to_parent_directory(get_current_directory())
    go_to_child_directory(SOURCE_DIRECTORY)

    generate_pdf()
    generate_bibliography()
    generate_pdf()


def generate_pdf() -> None:
    subprocess.call(
        [PDF_LATEX,
         "-file-line-error",
         "-interaction=nonstopmode",
         "-synctex=1",
         "-output-format=pdf",
         "-output-directory=../" + DIRECTORIES[1],
         "-aux-directory=../" + DIRECTORIES[0],
         TEX_FILENAME + TEX],
        shell=True
    )


def open_generated_pdf() -> None:
    go_to_parent_directory(get_current_directory())
    go_to_child_directory(DIRECTORIES[1])
    webbrowser.open(TEX_FILENAME + PDF)


def clean_project() -> None:
    go_to_parent_directory(get_current_directory())

    try:
        remove_directories(DIRECTORIES)
    except FileNotFoundError:
        print("Some directories may not be found!")

    go_to_child_directory(SOURCE_DIRECTORY)

    try:
        for it in FILE_EXTENSIONS:
            remove_files(glob.glob(it))
    except FileNotFoundError:
        print("Some files may not be found!")


def generate_bibliography() -> None:
    subprocess.call([BIBER, "../" + DIRECTORIES[0] + "/" + TEX_FILENAME], shell=True)


def remove_files(filenames: List[str]) -> None:
    for it in filenames:
        os.remove(it)


def remove_directories(directory_names: List[str]) -> None:
    for it in directory_names:
        shutil.rmtree(it)


def get_current_directory():
    return pathlib.Path(os.getcwd())


def go_to_parent_directory(directory) -> None:
    os.chdir(directory.parent)


def go_to_child_directory(directory: str) -> None:
    os.chdir(directory)


# UTIL ----------------------------------------------------------------------- #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-r", "--run", default=False, action="store_true", help="Run process of building pdf file"
    )
    arg_parser.add_argument(
        "-o", "--open", default=False, action="store_true", help="Open built pdf file"
    )
    arg_parser.add_argument(
        "-c", "--clean", default=False, action="store_true", help="Clean generated files"
    )

    return arg_parser.parse_args()


def run_main(main: Callable[[], None]) -> None:
    if check_if_exists_in_args("-t"):
        check_types()
    else:
        main()


def check_types() -> None:
    subprocess.call(["mypy", "."])


def check_if_exists_in_args(arg: str) -> bool:
    return arg in sys.argv


def display_finish() -> None:
    print("------------------------------------------------------------------------")
    print("FINISHED")
    print("------------------------------------------------------------------------")


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
