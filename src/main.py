from textnode import *
from htmlnode import *

print("hello world")


def main():

    t_type = TextType
    t_node = TextNode("This is some anchor text", t_type.LINK, "https://www.boot.dev") 

    print(t_node)


    html_a_example = HTMLNode("a", "a link to example.com", props={"href": "https://www.example.com/", "target": "_blank"})

    print(f"props for our node look like: |{html_a_example.props_to_html()}|")



main()
