from enum import Enum
from collections.abc import Callable
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    '''A limited list of our allowed Texttypes. We want to make sure only
    available formats are passed to our functions/methods'''
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode():
    '''a class to handle our Inline formats. Markdown text will be used to create
    objects, that then get formatted to HTML.'''
    def __init__(self, text:str, text_type:TextType, url:str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node:TextType) -> bool:
        '''"Is equal to" overload, to check, if two Nodes are the same.'''
        if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
            return True
        return False

    def __repr__(self) -> str:
        '''overload the stdout message to include needed information on an exception.'''
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise Exception("no Valid Texttype detected")
    if text_node.text_type is TextType.TEXT:
        return LeafNode(None,text_node.text)
    if text_node.text_type is TextType.BOLD:
        return LeafNode("b",text_node.text)
    if text_node.text_type is TextType.ITALIC:
        return LeafNode("i",text_node.text)
    if text_node.text_type is TextType.CODE:
        return LeafNode("code",text_node.text)
    if text_node.text_type is TextType.LINK:
        return LeafNode("a",text_node.text,{"href":text_node.url})
    if text_node.text_type is TextType.IMAGE:
        return LeafNode("img","",[{"src":text_node.url},{"alt":text_node.text}])