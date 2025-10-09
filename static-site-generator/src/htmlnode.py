#Don’t import converter.py or textnode.py

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        if not self.children:
            raise ValueError("missing children")

        props_str = ""
        if self.props:
            props_str = "".join(f' {k}="{v}"' for k, v in self.props.items())

        inner = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>" + inner + f"</{self.tag}>"

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        children_repr = self.children if self.children is None else f"<{len(self.children)} children>"
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={children_repr}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None): 
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All LeafNodes must have a value")
        if not self.tag:
            return self.value
        attribute_strings = []
        if self.props:
            for key, value in self.props.items():
                attribute_strings.append(f'{key}="{value}"')
        prop_attrs_str = " ".join(attribute_strings)
        formatted_props = f" {prop_attrs_str}" if prop_attrs_str else ""
        
        return f"<{self.tag}{formatted_props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        if not self.children:
            raise ValueError("missing children")

        props_str = ""
        if self.props:
            props_str = "".join(f' {k}="{v}"' for k, v in self.props.items())

        inner = "".join(child.to_html() for child in self.children)

        opening = f"<{self.tag}{props_str}>"
        closing = f"</{self.tag}>"

        return opening + inner + closing
