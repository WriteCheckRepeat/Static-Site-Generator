from enum import Enum
from collections.abc import Callable

class HTMLNode():
    '''This Class acts as a Parent Class for inheritance purposes. It's not supposed to be called directly.'''
    def __init__(self, tag:str = None, value:str = None, children = None, props:dict[str,str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("ERROR: Parentclass is not able to execute 'to_html' method")

    def props_to_html(self) -> str:
        if self.props is None: return ""
        html_attributes = ""
        for key, value in self.props.items():
            html_attributes += f' {key}="{value}"'
        return html_attributes

    def __repr__(self):
        '''overload the stdout message to include needed information.'''
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"

class LeafNode(HTMLNode):
    ''' A Leaf Node is at the very end of a HTML Node in a sense, that the
    tree doesn't continue from that point. This Node can't have a child attached'''
    def __init__(self, tag:str, value:str, props:dict[str,str] = None):
        super().__init__(tag=tag, value=value,  props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("ERROR: LeafNode is None.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props}"
    
class ParentNode(HTMLNode):
    ''' A Parent Node has Child Nodes. The Child nodes can be leaf nodes or different parent Nodes.'''

    def __init__(self, tag:str, children, props:dict[str,str] = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        if self.tag is None: raise ValueError("Error: Parent Node must have a tag")
        if self.children is None: raise ValueError("Error: Parent Node must have a child Node.")
        html_output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_output += child.to_html()
        html_output += f"</{self.tag}>"
        return html_output