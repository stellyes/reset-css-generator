import os
import time
from bs4 import BeautifulSoup

# The baseline tags to be modified by the BASELINE_CSS global
BASELINE_TAGS = ["html", "body", "div", "span", "applet", "object", "iframe", "h1", "h2",
                 "h3", "h4", "h5", "h6", "p", "blockquote", "pre", "a", "abbr", "acronym", 
                 "address", "big", "cite", "code", "del", "dfn", "em", "img", "ins", "kbd",
                 "q", "s", "samp", "small", "strike", "strong", "sub", "sup", "tt", "var",
                 "b", "u", "i", "center", "dl", "dt", "dd", "ol", "ul", "li", "fieldset",
                 "form", "label", "legend", "table", "caption", "tbody", "tfoot", "thead",
                 "tr", "th", "td", "article", "aside", "canvas", "details", "embed", "figure",
                 "figcaption", "footer", "header", "hgroup", "menu", "nav", "output", "ruby",
                 "section", "summary", "time", "mark", "audio", "video"]

# The CSS to modify the BASELINE_TAGS above
BASELINE_CSS = '''
                {
                    margin: 0;
                    padding: 0;
                    border: 0;
                    font-size: 100%;
                    font: inherit;
                    vertical-align: baseline;
                }
            '''

# Per reference.css, HTML5 display-role reset for older browsers 
DISPLAY_PROP_DEPRECATED_BROWSERS = ["article", "aside", "details", "figcaption", "figure",
                                    "footer", "header", "hgroup", "menu" "nav", "section"]

# Associated CSS for "HTML5 display-role reset for older browsers"
DISPLAY_CSS_DEPRECATED_BROWSERS = '''
                                    {
                                        display: block;
                                    }
                                '''

# Resets line height for body tag
LINE_HEIGHT_TAGS = ["body"]
LINE_HEIGHT_CSS = '''
                    {
                        display: block;
                    }   
                '''

# Resets list style for ordered and unordered lists
LIST_STYLE_TAGS = ["ol", "ul"]
LIST_STYLE_CSS = '''
                    {
                        list-style: none;
                    }
                '''

# Resets quote property for blockquotes, and :before and :after
# pseudo classes if the QUOTE_TAGS exist within the document
QUOTE_TAGS = ["blockquote", "q"]
QUOTE_CSS = '''
            {
                quotes: none;
            }
            '''
QUOTE_PSEUDO_CSS = '''
                    {
                        content: "";
                        content: none;
                    }
                '''

TABLE_BORDER_TAGS = ["table"]
TABLE_BORDER_CSS = '''
                    {
                    border-collapse: collapse;
                    border-spacing: 0;
                    }
                '''


def generateHeader(current_time):
    '''
    Takes in time.asctime object and generates a string to append to the 
    beginning of the reset.css file
    '''
    return "/*\n reset.css file generated on " + current_time + "\n\
            Script by Ryan England - Github: stellyes \n\
            \nTemplate for reset.css information: \n\
            http://meyerweb.com/eric/tools/css/reset/\n \
            v2.0 | 20110126\n \
            License: none (public domain)\n \
            */\n\n"
    
def buildTagList(tagList):

    tag_list_string = ""
    for tag in tagList:
        if tag is not tagList[len(tagList) - 1]:
            tag_list_string += tag + ",\n"
        else:
            tag_list_string += tag 

    return tag_list_string

def main():

    # Gather relative filepath to HTML doc from user
    print()
    filePath = input("Please enter relative file path to HTML document you wish to create a reset.css file for: ")

    while not os.path.exists(filePath):
        filePath = input("Invalid file path. Please try again: ")

    with open(filePath) as doc:
        soup = BeautifulSoup(doc, "html.parser")

    # Begin search for elements
    print("Succesfully loaded HTML document.")
    print("Generating reset.css document...")

    # Grab all HTML tags from document
    tagList = []
    for tag in soup.find_all(True):
        tagList.append(tag)

    # Remove duplicate tags in list
    tagList = list(set(tagList))

    # Format current time for file output
    current_time = str(time.asctime).replace(" ", "_")
    current_time = current_time.replace(":", "-")
    fileName = "output/reset_" + current_time + ".txt"

    # Initialized empty arrays to store corresponding and present tags
    # from HTML document. line_height_compare and table_compare are boolean
    # values since there's only one value to compare against in their lists
    baseline_compare = []
    display_compare = []
    line_height_compare = False
    list_style_compare = []
    quote_compare = []
    table_compare = False

    for tag in tagList:
        if tag in BASELINE_TAGS:
            baseline_compare.append(tag)
        elif tag in DISPLAY_PROP_DEPRECATED_BROWSERS:
            display_compare.append(tag)
        elif tag in LINE_HEIGHT_TAGS:
            line_height_compare = True
        elif tag in LIST_STYLE_TAGS:
            list_style_compare.append(tag)
        elif tag in QUOTE_TAGS:
            quote_compare.append(tag)
        elif tag in TABLE_BORDER_TAGS:
            table_compare = True

    with open(fileName, 'w') as file:
        # Write header to file
        file.write(generateHeader(current_time)) 

        if baseline_compare != []:
            file.write(buildTagList(baseline_compare))
            file.write(BASELINE_CSS)
            file.write("\n\n")

        if display_compare != []:
            file.write(buildTagList(display_compare))
            file.write(DISPLAY_CSS_DEPRECATED_BROWSERS)
            file.write("\n\n")
        
        if line_height_compare:
            file.write("body ")
            file.write(LINE_HEIGHT_CSS)
            file.write("\n\n")

        if quote_compare != []:
            file.write(buildTagList(quote_compare))
            file.write(QUOTE_CSS)
            file.write("/n/n")
            for tag in quote_compare:
                if len(quote_compare) == 1:
                    file.write(quote_compare[0] + ":before, \n" + quote_compare[0] + ":after ")
                else:
                    file.write(quote_compare[0] + ":before, \n" + quote_compare[0] + ":after, \n " + \
                               quote_compare[1] + ":before, \n" + quote_compare[0] + ":after ")
            file.write(QUOTE_PSEUDO_CSS)
            file.write("\n\n")

        if table_compare:
            file.write("table ")
            file.write(TABLE_BORDER_CSS)

