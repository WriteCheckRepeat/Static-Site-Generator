from textnode import TextNode
from textnode import TextType

def main():
    dummy = TextNode("This is some anchor text",TextType.LINKS , "https://www.boot.dev")
    print(dummy)

main()