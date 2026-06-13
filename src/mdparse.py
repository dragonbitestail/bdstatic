from enum import Enum
from textnode import *
import logr
import re

import time

#logr.DEBUG=True
logr.DEBUG=False

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE   = "quote"
    UNORDERED_LIST   = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    logr.log(f"split_nodes_delimiter(): old_nodes: {old_nodes}")

    new_nodes = []

    for node in old_nodes:
        logr.log(f"split_nodes_delimiter(): old_node text: {node.text}")

        delims_count = node.text.count(delimiter)
        logr.log(f"node.text final delims_count: {delims_count}")
        if delims_count % 2 != 0:
            raise Exception("Invalid markdown: unbalanced delimiters found")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            logr.log(f"node parts: {parts}")
            for i in range(0, len(parts)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                elif parts[i] != "":
                    logr.log(f"Using i {i} to add |{parts[i]}| as new {text_type} node")
                    new_nodes.append(TextNode(parts[i], text_type))

    logr.log(f"split_nodes_delimiter(): return : {new_nodes}")
    return new_nodes

def extract_markdown_images(text: str) -> tuple[str, str]:

    matches = re.findall(r"!\[([^\]]+)\]\(([^\)]+)\)", text)
    logr.log(f"extract_markdown_images(): matches: {matches}")

    return matches


def extract_markdown_links(text: str) -> tuple[str, str]:

    matches = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", text)
    logr.log(f"extract_markdown_links(): matches: {matches}")

    return matches


# From Boot.Dev Solution: CH3, L3 Split Images and links
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def OLD_split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    logr.log(f"split_nodes_image(): old_nodes: {old_nodes}")

    new_nodes = []

    for node in old_nodes:
        logr.log(f"split_nodes_image(): old_node text: \"{node.text}\" of type \"{node.text_type}\"")
        if node.text_type != TextType.TEXT or len(extract_markdown_images(node.text)) < 1:
            new_nodes.append(node)
            continue

        i = 0
        while i < len(node.text):

            logr.log(f"split_nodes_image(): OUTER while(): char \"{node.text[i]}\" <<<<<<<<<<<<<<<<<<<<<<")
            new_alt = ""
            new_url = ""
            new_text = ""

            # We are at last char, this cannot be an image link
            if i + 1 == len(node.text):
                new_nodes.append(node)
                break
            if node.text[i] == "!" and node.text[i+1] == "[":
                i += 2
                logr.log(f"split_nodes_image(): accumulating alt text starting with char {node.text[i]} ![......................")
                while i < len(node.text) and node.text[i] != "]":
                    new_alt += node.text[i]
                    i += 1

                i += 1
                if node.text[i] == "(":
                    i += 1
                else:
                    next
                logr.log(f"split_nodes_image(): accumulating url text starting with char {node.text[i]} (.......................")
                while i < len(node.text) and node.text[i] != ")":
                    new_url += node.text[i]
                    i += 1
                new_nodes.append(TextNode(new_alt, TextType.IMAGE, url=new_url))
                i += 1
            elif i + 1 < len(node.text) and node.text[i + 1] != "[":
                i += 1
            else:
                logr.log(f"split_nodes_image(): accumulating plain text starting with char {node.text[i]} TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                #while i < len(node.text) and node.text[i] != "!":
                if i + 1 == len(node.text) and node.text[i] != "[" :
                    logr.log(f"split_nodes_image(): BREAK on {node.text[i]}; end of string.")
                    new_text += node.text[i]
                    i += 1
                    break
                while i < len(node.text) and node.text[i] != "!":
                    new_text += node.text[i]
                    i += 1
                new_nodes.append(TextNode(new_text, TextType.TEXT))

            #time.sleep(2)
            logr.log(f"split_nodes_image(): BOTTOM of OUTER while loop: new_nodes: {new_nodes}")


    logr.log(f"split_nodes_image(): return : {new_nodes} ***************************************")
    return new_nodes

# From Boot.Dev Solution: CH3, L3 Split Images and links
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def OLD_split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    logr.log(f"split_node_link(): old_nodes: {old_nodes}")

    new_nodes = []

    for node in old_nodes:
        logr.log(f"split_node_link(): old_node text: {node.text} of type {node.text_type}")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        i = 0
        while i < len(node.text):

            logr.log(f"split_node_link(): evaluating char {node.text[i]} <<<<<<<<<<<<<<<<<<<<<<")
            new_alt = ""
            new_url = ""
            new_text = ""
            if node.text[i] == "[":
                i += 1
                logr.log(f"split_node_link(): accumulating alt text starting with char {node.text[i]} [......................")
                while node.text[i] != "]":
                    new_alt += node.text[i]
                    i += 1

                i += 1
                if node.text[i] == "(":
                    i += 1
                else:
                    next
                logr.log(f"split_node_link(): accumulating url text starting with char {node.text[i]} (.......................")
                while node.text[i] != ")":
                    new_url += node.text[i]
                    i += 1
                new_nodes.append(TextNode(new_alt, TextType.LINK, url=new_url))
                i += 1
            else:
                logr.log(f"split_node_link(): accumulating plain text starting with char {node.text[i]} TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                while i < len(node.text):
                    if node.text[i] == "[":
                        break
                    new_text += node.text[i]
                    i += 1

                new_nodes.append(TextNode(new_text, TextType.TEXT))


    logr.log(f"split_node_link(): return : {new_nodes} ***************************************")
    return new_nodes


def text_to_textnodes(text):
    logr.log(f"text_to_textnodes(): IN: {text}")
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)


    logr.log(f"text_to_textnodes(): OUT: {new_nodes}")
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = []

    logr.log(f"markdown_to_blocks: START: ==============================")
    for block in markdown.split("\n\n"):
        logr.log(f"{block}")
        #stripped_block = " ".join(block.split())
        #blocks.append(stripped_block)
        blocks.append(block.strip())

    logr.log(f"markdown_to_blocks: STOP: ==============================")

    return blocks

def block_to_block_type(block):
    logr.log(f"block_to_block_type: IN:\n{block}")

    block_type = BlockType.PARAGRAPH

    r_heading = re.compile(r"^[#]{1,6}")

    # Must match across lines
    r_mlcode = re.compile(r"^[`]{3}\n.+[`]{3}$", re.DOTALL)

    # These required parse block by lines to eval each line for pattern:
    r_qblock_start = re.compile(r"^[>]", re.MULTILINE)
    r_unord_block_start = re.compile(r"^[-] ", re.MULTILINE)

    # same as above but, also requires check of sequence of start is valid:
    r_ord_block_start = re.compile(r"^([\d]+)\. ")

    if r_heading.match(block):
        logr.log(f"block_to_block_type(): We have a heading block ####################")
        block_type = BlockType.HEADING
    elif r_mlcode.match(block):
        logr.log(f"block_to_block_type(): We have a multiline code block ````````````````````")
        block_type = BlockType.CODE
    elif r_qblock_start.match(block):
        logr.log(f"block_to_block_type(): We have a **possible** quote block >>>>>>>>>>>>>>>>>>>>")
        block_type = BlockType.QUOTE
    elif r_unord_block_start.match(block):
        logr.log(f"block_to_block_type(): We have a **possible** unordered_list block - - - - - - - - - -")
        block_type = BlockType.UNORDERED_LIST
    elif r_ord_block_start.match(block) and all_lines_ordered(r_ord_block_start, block):
        logr.log(f"block_to_block_type(): We have a **possible** ordered_list block N.N.N.N.N.N.N.N.N.N.")
        block_type = BlockType.ORDERED_LIST

    logr.log(f"block_to_block_type(): OUT: block_type: {block_type}")
    return block_type


def all_lines_ordered(re_obj, block):
    lines_ordered = True
    last_num = None
    for line in block.split("\n"):
        cur_num = int(re_obj.match(line).group(1))
        logr.log(f"all_lines_ordered(): eval'ing line: {line} w/ cur_num: {cur_num}")
        if last_num == None:
            last_num = cur_num
            continue
        if cur_num - 1 != last_num:
            lines_ordered = False
            break
        last_num = cur_num

    logr.log(f"all_lines_ordered(): OUT: lines_ordered: {lines_ordered}")
    return lines_ordered
