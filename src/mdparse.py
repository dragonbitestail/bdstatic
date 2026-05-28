from enum import Enum
from textnode import *

DEBUG=True

def log(msg):

    DEBUG and print(f"[DEBUG] {msg}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    log(f"split_nodes_delimiter(): old_nodes: {old_nodes}")

    new_nodes = []

    for node in old_nodes:
        log(f"split_nodes_delimiter(): old_node text: {node.text}")

        delims_count = node.text.count(delimiter)
        log(f"node.text final delims_count: {delims_count}")
        if delims_count % 2 != 0:
            raise Exception("Invalid markdown: unbalanced delimiters found")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            log(f"node parts: {parts}")
            for i in range(0, len(parts)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    log(f"Using i {i} to add |{parts[i]}| as new {text_type} node")
                    new_nodes.append(TextNode(parts[i], text_type))

    log(f"split_nodes_delimiter(): return : {new_nodes}")
    return new_nodes
