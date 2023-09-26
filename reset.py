import os
import time
import cssutils
from bs4 import BeautifulSoup

HEADER = '''
/*
    Script by Ryan England - Github: stellyes
    https://github.com/stellyes/reset-css-generator
                
    Template for reset.css information:
    http://meyerweb.com/eric/tools/css/reset/
    v2.0 | 20110126
    License: none (public domain)
*/
'''

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
    
def buildTagList(tagList):

    tag_list_string = ""
    for tag in tagList:
        if tag is not tagList[len(tagList) - 1]:
            tag_list_string += tag + ",\n "
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
        if tag.name not in tagList:
            tagList.append(tag.name)

    # Remove duplicate tags in list
    tagList = list(set(tagList))

    # Initialized empty arrays to store corresponding and present tags
    # from HTML document. line_height_compare and table_compare are boolean
    # values since there's only one value to compare against in their lists
    baseline_compare = []
    display_compare = []
    line_height_compare = False
    list_style_compare = []
    quote_compare = []
    table_compare = False

    # Building out css file by testing for tags in each
    # serction of the reference document
    for tag in tagList:
        if tag in BASELINE_TAGS:
            baseline_compare.append(tag)

        if tag in DISPLAY_PROP_DEPRECATED_BROWSERS:
            display_compare.append(tag)
        
        if tag in LINE_HEIGHT_TAGS:
            line_height_compare = True
        
        if tag in LIST_STYLE_TAGS:
            list_style_compare.append(tag)
        
        if tag in QUOTE_TAGS:
            quote_compare.append(tag)
        
        if tag in TABLE_BORDER_TAGS:
            table_compare = True

    # Writing structured css to file
    css_string = HEADER

    if baseline_compare != []:
        css_string += buildTagList(baseline_compare) + BASELINE_CSS + "\n\n"

    if display_compare != []:
        css_string += buildTagList(display_compare) + DISPLAY_CSS_DEPRECATED_BROWSERS + "\n\n"
    
    if line_height_compare:
        css_string += "body " + LINE_HEIGHT_CSS + "\n\n"

    if quote_compare != []:
        css_string += buildTagList(quote_compare) + QUOTE_CSS + "/n/n"
        for tag in quote_compare:
            if len(quote_compare) == 1:
                css_string += quote_compare[0] + ":before, \n" + quote_compare[0] + ":after "
            else:
                css_string += quote_compare[0] + ":before, \n" + quote_compare[0] + ":after, \n " + \
                            quote_compare[1] + ":before, \n" + quote_compare[0] + ":after "
        css_string += QUOTE_PSEUDO_CSS
        css_string += "\n\n"

    if table_compare:
        css_string += "table "
        css_string += TABLE_BORDER_CSS

    css_code = cssutils.parseString(css_string)
    current_time = time.ctime().lower()
    current_time = current_time.replace(" ", "_")

    with open("output/reset_" + current_time + ".css", "w") as css:
        raw_css = str(css_code.cssText.decode('ascii')).replace(",", ",\n")
        css.write(raw_css)

    print("reset.css file generated! Please refer to reset.css file in the output  \
           folder with the current date and time.")


if __name__ == "__main__":
    main()