from enum import Enum
from textnode import *
from htmlnode import *
from mdparse import *
import logr
import re

#logr.DEBUG=True
logr.DEBUG=False

def markdown_to_html_node(markdown):
    p_children = []

    for block in markdown_to_blocks(markdown):
        if not block:
            logr.log(f"markdown_to_html_node: skipping empty block....")
            continue

        logr.log(f"markdown_to_html_node: parsing block\n{block}")
        b_type = block_to_block_type(block)
        logr.log(f"markdown_to_html_node: block type determined as: {b_type}")

        stripped_block = ""

        if b_type != BlockType.CODE:
            stripped_block = " ".join(block.split())

        if b_type == BlockType.CODE:
            p_children.append(code_block_to_html_node(block))
        elif b_type == BlockType.PARAGRAPH:
            para_node = create_para_node(stripped_block)
            logr.log(f"markdown_to_html_node: appending to p_children; para_node: {para_node}")
            p_children.append(para_node)
        elif b_type == BlockType.HEADING:
            h_level = block.count("#")
            block = block.split("#")[-1].strip()
            logr.log(f"markdown_to_html_node: count # in block {h_level} before clean to {block} HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            header = LeafNode(tag=f"h{h_level}", value=block)
            p_children.append(header)
        elif b_type == BlockType.QUOTE:
            logr.log(f"markdown_to_html_node: handling creating of blockquote")
            filtered_block = re.sub(r"^>\s*", '', block, flags=re.MULTILINE)
            bquote = LeafNode(tag="blockquote", value=filtered_block)
            p_children.append(bquote)
        elif b_type == BlockType.UNORDERED_LIST or b_type == BlockType.ORDERED_LIST:
            list_node = generate_html_list(block)
            p_children.append(list_node)
        else:
            child_nodes = generate_html_children(stripped_block)
            para_with_childs = ParentNode(tag="p", children=child_nodes)
            p_children.append(para_with_childs)

    p_node = ParentNode(tag="div", children=p_children)

    return p_node


def generate_html_list(md_block):

    if md_block.startswith("- "):
        logr.log(f"generate_html_list(): we have unordered_list")
        l_tag="ul"
    elif md_block[0].isdigit():
        logr.log(f"generate_html_list(): we have ordered_list")
        l_tag="ol"

    l_items = []
    for line in md_block.split("\n"):
        stripped_line = re.sub(r"^(-|\d+\.)\s+", '', line, flags=re.MULTILINE)
        child_nodes = generate_html_children(stripped_line)
        l_item = ParentNode(tag="li", children=child_nodes)
        l_items.append( l_item )

    list_node = ParentNode(tag=l_tag, children=l_items)

    return list_node


def create_para_node(stripped_block: str) -> ParentNode:
    logr.log(f"create_para_node: creating children for paragraph stripped_block {stripped_block}")
    child_nodes = generate_html_children(stripped_block)
    return ParentNode(tag="p", children=child_nodes)


def generate_html_children(text: str) -> list[LeafNode]:
    l_nodes = []

    for text_node in text_to_textnodes(text):
        # convert to html node
        logr.log(f"generate_html_children: convert text_node: {text_node} to HTML LeafNode")
        l_node = text_node_to_html_node(text_node)
        logr.log(f"generate_html_children: result of text_node converted to l_node: {l_node}")
        l_nodes.append(l_node)

    return l_nodes


def code_block_to_html_node(block):
    # Strip leading and trailing ``` from markdown code block
    filtered_block = block.lstrip("``` \n").rstrip("``` ")
    logr.log(f"code_block_to_html_node: filtered_block: {filtered_block}")

    # Convert to CODE TextNode
    t_code_node = TextNode(filtered_block, TextType.CODE)
    # Convert to CODE HTMLNode
    html_code_node = text_node_to_html_node(t_code_node)

    # Create html pre container for the LeafNode code node and add as child:
    html_pre_code_node = ParentNode(tag="pre", children=[html_code_node])

    logr.log(f"code_block_to_html_node: return: html_pre_code_node.to_html:\n{html_pre_code_node.to_html()}")
    return html_pre_code_node
