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

def block_to_html(block, block_type):
    text = block.split("\n")
    #text = block
    match block_type:
        case BlockType.PARAGRAPH:
            raw_lines = text
            return [ParentNode("p", lines_to_html_nodes([l])) for l in raw_lines]
        case BlockType.HEADING:
            n = text[0].split(" ")[0].count("#")
            raw_lines = [re.sub(r"^#{1,6} ", "", l) for l in text]
            raw_lines = [x for x in raw_lines if x]
            return [ParentNode(f"h{n}", lines_to_html_nodes([l])) for l in raw_lines]
        case BlockType.QUOTE:
            raw_lines = [re.sub(r"^>", "", l) for l in text]
            raw_lines = [x for x in raw_lines if x]
            return [ParentNode("blockquote", lines_to_html_nodes([l])) for l in raw_lines]
        case BlockType.CODE:
            raw_lines = [re.sub(r"^`{3}", "", l) for l in text]
            raw_lines = [x for x in raw_lines if x]
            #return [ParentNode("code", lines_to_html_nodes([l])) for l in raw_lines]
            return ParentNode("code", lines_to_html_nodes(raw_lines)) 
        case BlockType.UNLIST:
            raw_lines = [re.sub(r"^\*|- ", "", l) for l in text]
            raw_lines = [x for x in raw_lines if x]
            child_nodes = [ParentNode("li", lines_to_html_nodes([l])) for l in raw_lines]
            return ParentNode("ul", child_nodes)
        case BlockType.OLIST:
            raw_lines = [re.sub(r"^\d+. ", "", l) for l in text]
            raw_lines = [x for x in raw_lines if x]
            child_nodes = [ParentNode("li", lines_to_html_nodes([l])) for l in raw_lines]
            return ParentNode("ol", child_nodes)
        case _:
            raise ValueError("Please provide a valid block type")
               

def markdown_to_html_node(text):
    text = markdown_to_blocks(text)
    nodes = []
    for block in text:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p",children=block_to_html(block, block_type)))
            case BlockType.HEADING:
                nodes.append(ParentNode(f"h{block[5].count("#")}",children=block_to_html(block, block_type)))
            case BlockType.QUOTE:
                nodes.append(ParentNode("blockquote", children=block_to_html(block, block_type)))
            case BlockType.CODE:
                nodes.append(HTMLNode("code", children=block_to_html(block, block_type)))
            case BlockType.UNLIST:
                child_nodes = [LeafNode("li", node) for node in block_to_html(block, block_type)]
                nodes.append(ParentNode("ul", child_nodes))
            case BlockType.OLIST:
                child_nodes = [LeafNode("li", node) for node in block_to_html(block, block_type)]
                nodes.append(ParentNode("ol", child_nodes))
    return ParentNode("div", nodes)