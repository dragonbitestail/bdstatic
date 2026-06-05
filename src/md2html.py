from enum import Enum
from textnode import *
from htmlnode import *
from mdparse import *
import re

#DEBUG=True
DEBUG=False

def log(msg):

    DEBUG and print(f"[DEBUG] {msg}")


def markdown_to_html_node(markdown):
    p_children = []

    for block in markdown_to_blocks(markdown):
        if not block:
            log(f"markdown_to_html_node: skipping empty block....")
            continue

        log(f"markdown_to_html_node: parsing block\n{block}")
        b_type = block_to_block_type(block)
        log(f"markdown_to_html_node: block type determined as: {b_type}")

        if b_type != BlockType.CODE:
            stripped_block = " ".join(block.split())

        if b_type == BlockType.CODE:
            p_children.append(code_block_to_html_node(block))
        elif b_type == BlockType.PARAGRAPH:
            para_node = create_para_node(stripped_block)
            log(f"markdown_to_html_node: appending to p_children; para_node: {para_node}")
            p_children.append(para_node)
        else:
            child_nodes = generate_html_children(stripped_block)
            p_children.extend(child_nodes)

    p_node = ParentNode(tag="div", children=p_children)

    return p_node


def create_para_node(stripped_block: str) -> ParentNode:
    log(f"create_para_node: creating children for paragraph stripped_block {stripped_block}")
    child_nodes = generate_html_children(stripped_block)
    return ParentNode(tag="p", children=child_nodes)


def generate_html_children(text: str) -> list[LeafNode]:
    l_nodes = []

    for text_node in text_to_textnodes(text):
        # convert to html node
        log(f"generate_html_children: convert text_node: {text_node} to HTML LeafNode")
        l_node = text_node_to_html_node(text_node)
        log(f"generate_html_children: result of text_node converted to l_node: {l_node}")
        l_nodes.append(l_node)

    return l_nodes


def code_block_to_html_node(block):
    # Strip leading and trailing ``` from markdown code block
    filtered_block = block.lstrip("``` \n").rstrip("``` ")
    log(f"code_block_to_html_node: filtered_block: {filtered_block}")

    # Convert to CODE TextNode
    t_code_node = TextNode(filtered_block, TextType.CODE)
    # Convert to CODE HTMLNode
    html_code_node = text_node_to_html_node(t_code_node)

    # Create html pre container for the LeafNode code node and add as child:
    html_pre_code_node = ParentNode(tag="pre", children=[html_code_node])

    #html_pre_code_node = text_node_to_html_node(html_pre_node)
    log(f"code_block_to_html_node: return: html_pre_code_node.to_html:\n{html_pre_code_node.to_html()}")
    return html_pre_code_node
