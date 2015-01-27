from sikuli import *

def export_select():
    if exists(Pattern("detect_computer.png").exact()):
        click(Pattern("click_projector.png").exact())
    elif exists("detect_projector.png"):
        click(Pattern("click_computer.png").exact())
           
        