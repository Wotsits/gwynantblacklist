import re

def clean(reg):
 
 
    #convert reg to upper
    reg = reg.upper()
 
    #remove any spaces
    reg = reg.replace(' ', '')
    reg = reg.replace('-', '')
 
    #check for any common invalid characters
    regex = re.compile('[.,!"£$%^&*()_+=}{:;@#|?]')
    if regex.search(reg) == None:
        pass
 
    #check that the reg length is valid
    if len(reg) <= 7:
        pass
    else:
        if "," in reg:
            reg = reg.split(",")
        if "/" in reg:
            reg = reg.split("/")
        if "\\" in reg:
            reg = reg.split("\\")

    return reg