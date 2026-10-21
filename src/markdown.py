from collections.abc import Callable
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    tag_map = {
    "'":TextType.CODE,
    "**":TextType.BOLD,
    "_":TextType.ITALIC
    }
    for old_node in old_nodes:
        if old_node.text_type is not text_type.TEXT:
            new_nodes.append(old_node)
        else:
            tmp_strs = old_node.text.split(delimiter)
            if len(tmp_strs)%2:
                raise Exception(f"Error: Missing a closing '{delimiter}' in '{old_node}'")
            inside_inline = False
            for i in range(len(tmp_strs)):
                if inside_inline:
                    new_nodes.append(TextNode(tmp_strs[i],tag_map[delimiter]))
                    inside_inline = False
                else:
                    new_nodes.append(TextNode(tmp_strs[i],TextType.TEXT))
                    inside_inline = True
