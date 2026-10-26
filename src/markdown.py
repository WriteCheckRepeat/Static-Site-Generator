from collections.abc import Callable
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    '''
    Syntax to split Lists of Text Nodes with markdown delimiters to Text Node Types. This Function only handles
    Text formats like Bold and Italic. It's not used for Links and Images. 
    '''
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            tmp_strs = old_node.text.split(delimiter)
            if not len(tmp_strs)%2:
                raise Exception(f"Error: Missing a closing '{delimiter}' in '{old_node}'")
            inside_inline = False
            for i in range(len(tmp_strs)):
                if inside_inline:
                    new_nodes.append(TextNode(tmp_strs[i],text_type))
                    inside_inline = False
                else:
                    new_nodes.append(TextNode(tmp_strs[i],TextType.TEXT))
                    inside_inline = True
    return new_nodes

def extract_markdown_images(text:str) -> list[tuple]:
    '''Placeholder description.
    '''
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text:str) -> list[tuple]:
    '''Placeholder description.
    '''
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)