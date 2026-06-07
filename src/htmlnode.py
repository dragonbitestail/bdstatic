import logr

#logr.DEBUG=True


class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # Expected to be overridden in child classes.
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        props_parts = [""]
        for k in self.props:
            props_parts.append(f"{k}=\"{self.props[k]}\"")

        return " ".join(props_parts)

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):

        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        props_str = self.props_to_html()

        tag_start = f"<{self.tag}{props_str}"
        tag_close = f">{self.value}</{self.tag}>"
        if self.value == "":
            tag_close = " />"

        final_html = f"{tag_start}{tag_close}"

        logr.log(f"LeafNode.to_html(): return: {final_html}")
        return final_html

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):

        if self.tag == "" or self.tag is None:
            raise ValueError("All parent nodes must have a tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have at least one child in children")

        props_str = self.props_to_html()
        final_html = f"<{self.tag}{props_str}>"
        for child in self.children:
            logr.log(f"ParentNode.to_html(): calling child {child}")
            final_html += child.to_html()

        final_html += f"</{self.tag}>" 
        logr.log(f"ParentNode.to_html(): return: {final_html}")
        return final_html


    def __repr__(self):
        return f"tag: {self.tag}, children: {self.children}, props: {self.props}"
