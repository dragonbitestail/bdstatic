from textnode import *
from htmlnode import *
from mdparse import *
from md2html import *
from os import listdir, path, mkdir, makedirs
from shutil import copy, rmtree
from sys import argv
import logr

#logr.DEBUG=True
logr.DEBUG=False

def purge_dir(dir_path: str, recreate_dir: bool=False):
    if path.isdir(dir_path):
        logr.log(f"purge_dir: removing dir_path: {dir_path}")
        rmtree(dir_path)

    if recreate_dir:
        logr.log(f"purge_dir: recreating dir_path: {dir_path}")
        mkdir(dir_path)


def copy_dir(src_path: str, dest_path: str, delete_dest: bool=False):
    logr.log(f"copy_dir: src_path: {src_path}, dest_path: {dest_path}, delete_dest: {delete_dest}")

    if delete_dest:
        purge_dir(dest_path, recreate_dir=True)

    r_copy(src_path, dest_path)


def r_copy(src_path, dest_path, file=None):

    logr.log(f"r_copy: src_path: {src_path}, dest_path: {dest_path}, file: {file}")
    # Open src_path to get dirs in src_path
    for file in listdir(src_path):
        logr.log(f"r_copy: eval'ing file: {file}")
        # Full path to src file (path + file)
        src_file = path.join(src_path, file)

        # For each regular file in src_path, copy to dest
        if path.isfile(src_file):
            logr.log(f"r_copy: copy'ing {src_file} to {dest_path}")
            if not path.exists(dest_path):
                mkdir(dest_path)
            copy(path.join(src_path, file), dest_path)
        elif path.isdir(src_file):
            # For each dir file in src_path, copy to dest then recurse
            logr.log(f"r_copy: recursive call for directory {src_file} to {dest_path}")
            r_copy( src_file, path.join(dest_path, file))


def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        b_type = block_to_block_type(block)
        logr.log(f"extract_title(): block: {block}, type: {b_type}")
        if b_type == BlockType.HEADING:
            return block.split("#")[1].strip()

    raise Exception("title block not found")

def generate_page(from_path, template_path, dest_path, basepath):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_file = ""
    template_file = ""
    with open(from_path, "r") as r_file:
        md_file = r_file.read()

    html_title = extract_title(md_file)

    with open(template_path, "r") as r_file:
        template_file = r_file.read()

    html_content = ""
    for block in markdown_to_blocks(md_file):
        b_type = block_to_block_type(block)
        logr.log(f"generate_page(): b_type: {b_type}, block: {block} to be converted to html...")

        block_as_html = markdown_to_html_node(block).to_html()
        if b_type != BlockType.CODE:
            # replace all root basepath '/' with optional basepath whose default is '/' for href and src
            block_as_html = re.sub("(href|src)=\"/", r'\1="{}'.format(basepath), block_as_html)

        logr.log(f"generate_page(): appending block as html {block_as_html} to html_content...")

        html_content += block_as_html

    logr.log(f"replacing title: {html_title} in template")
    rendered_template = template_file.replace("{{ Title }}", html_title)
    rendered_template = rendered_template.replace("{{ Content }}", html_content)

    write_file(dest_path, rendered_template)


def write_file(dest_path, file_contents):
    path_parts = path.split(dest_path)

    if len(path_parts) > 0 and not path.exists(path_parts[0]):
        try:
            makedirs(dest_path[0])
        except FileExistsError as f_except:
            print(f"FileExistsError: {f_except}")

    with open(dest_path, "w") as f_out:
        f_out.write(file_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    logr.log(f"generate_pages_recursive: dir_path_content: \"{dir_path_content}\", template_path: \"{template_path}\", dest_dir_path: \"{dest_dir_path}\"")

    # Open dir_path_content to get dirs in dir_path_content
    for file in listdir(dir_path_content):
        logr.log(f"generate_pages_recursive: eval'ing file: \"{file}\" in \"{dir_path_content}\"")
        # construct full path to src file and dest file relative to dest_dir_path
        src_file = path.join(dir_path_content, file)
        dst_file = path.join(dest_dir_path, file)

        # For each markdown file in dir_path_content, generate html beneath dest_dir_path
        if path.isfile(src_file) and src_file.endswith(".md"):
            logr.log(f"generate_pages_recursive: generating \"{src_file}\" to \"{dst_file}\"")
            generate_page(src_file, template_path, dst_file[:-3] + ".html", basepath)
        elif path.isdir(src_file):
            # remove target prior to re-generating
            if path.isdir(dst_file):
                purge_dir(dst_file, recreate_dir=True)
            elif not path.exists(dst_file):
                logr.log(f"generate_pages_recursive: MKDIR-MKDIR-MKDIR-MKDIR-MKDIR creating dir \"{dest_dir_path}\" for \"{dst_file}\" to live in...")
                mkdir(dst_file)


            # For each dir file in dir_path_content, copy to dest then recurse
            logr.log(f"generate_pages_recursive: recursive call for source directory \"{file}\"")
            generate_pages_recursive(src_file, template_path, dst_file, basepath)


def main():

    t_type = TextType
    t_node = TextNode("This is some anchor text", t_type.LINK, "https://www.boot.dev")

    print(t_node)


    html_a_example = HTMLNode("a", "a link to example.com", props={"href": "https://www.example.com/", "target": "_blank"})

    print(f"props for our node look like: |{html_a_example.props_to_html()}|")


    # if we have a command line arg, assume it is basepath for our web site anchor links:
    basepath = '/'
    target_dir = './docs'
    if len(argv) == 2:
        basepath = argv[1]
    if len(argv) == 3:
        basepath = argv[1]
        target_dir = argv[2]

    copy_dir("./static", target_dir, delete_dest=True)

    print(f"target_dir: {target_dir} with basepath: {basepath} for href & src tags <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    generate_pages_recursive("./content", "./template.html", target_dir, basepath)

main()
