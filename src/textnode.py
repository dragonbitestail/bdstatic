from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE   = "code"
    LINK   = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, text_node):

        is_equal = False

        if (self.text == text_node.text and
            self.text_type == text_node.text_type and
            self.url == text_node.url):
            is_equal = True

        return is_equal


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            #link_parts = text_node.text.split("](")
            #value = link_parts[0][1:]
            #url = link_parts[1][:-1]
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            #link_parts = text_node.text.split("](")
            #descr = link_parts[0][2:]
            #url = link_parts[1][:-1]
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

        case _:
            raise Exception("unkown TextNode type")
