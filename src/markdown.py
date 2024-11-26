from textnode import *
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNLIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(text):
    #text to blocks
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, text.strip())

def block_to_block_type(text):
    heading_regex = r"(?m)^#{1,6} .+" #every line starts with
    code_regex = r"^`{3}[\S\s]*?`{3}$" #first and last line equal to
    quote_rexex = r"(?m)^>.*"#matches should = number of lines
    unordered_regex = r"(?m)^\*|- .+"#every line starts with
    #x=1
    #ordered_regex = rf"^{x}+\. " #every line starts with + increments
    x = re.findall(heading_regex, text)
    if len(re.findall(heading_regex, text)) == len(text.split("\n")):
        return BlockType.HEADING
    elif re.match(code_regex, text):
        return BlockType.CODE
    elif len(re.findall(quote_rexex, text)) == len(text.split("\n")):
        return BlockType.QUOTE
    elif len(re.findall(unordered_regex, text)) == len(text.split("\n")):
        return BlockType.UNLIST
    elif all([re.findall(rf"^{i + 1}\. ", x) for i, x in enumerate(text.split("\n"))]):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def block_to_children(text, block_type):
    text = text.split("\n")
    match block_type:
        case BlockType.PARAGRAPH:
            pass
        case BlockType.HEADING:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.CODE:
            pass
        case BlockType.UNLIST:
            pass
        case BlockType.OLIST:
           #parse through every line and remove the identifiers (numbers maybe using regex)
           # and make child nodes of type li
           #create parent html node of the type ol 
           #append to results
           #text_to_html(text)
    

#def markdown_to_html_node(text):
#    text = markdown_to_blocks(text)
#    nodes = []
#    for block in text:
#        block_type = block_to_block_type(block)
#        match block_type:
#            case BlockType.PARAGRAPH:
#                nodes.append(HTMLNode("p",block))
#            case BlockType.HEADING:
#                nodes.append(HTMLNode(f"h{block[5].count("#")}",block.split(f"{block[5].count("#")}").join("")))
#            case BlockType.QUOTE:
#                nodes.append(HTMLNode("blockquote", block.split(">").join("")))
#            case BlockType.CODE:
#                nodes.append(HTMLNode("code", block.strip("```")))
#            case BlockType.UNLIST:
#                child_nodes = [LeafNode("li", node) for node in nodes.split("\n")]
#                nodes.append(ParentNode("ul", child_nodes))
#            case BlockType.OLIST:
#                child_nodes = [LeafNode("li", node) for node in nodes.split("\n")]
#                nodes.append(ParentNode("ol", child_nodes))
