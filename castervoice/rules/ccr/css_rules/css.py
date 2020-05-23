from castervoice.lib.actions import Key, Text
from castervoice.lib import settings, printer
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST

from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


# HTML auto complete workaround for Jetbrains Products
# If more applications have issues with auto complete may be moved to actions.py
_context = AppContext(executable=["idea", "idea64", "studio64", "pycharm", "webstorm64", "webstorm"])

if _context:
    from dragonfly.actions.action_paste import Paste as Text
    if settings.settings(["miscellaneous", "use_aenea"]):
        try:
            from aenea import Paste as Text
        except ImportError:
            printer.out("Unable to import aenea Paste actions. Dragonfly actions will be used "
                  "instead.")
else:
    from castervoice.lib.actions import Text


class CSS(MergeRule):
    pronunciation = "css"

    mapping = {
        #Macros
        "selector":
            R(Text("{}") + Key("left/10:1") + Key("enter")),
        "property":
            R(Text(":;") + Key("left/10:1")),
        #Measurements
        "<ln1> pixel | <ln1> PX":
            R(Text("%(ln1)spx")),
        "<ln1> percentage | <ln1> percent":
            R(Text("%(ln1)s") + Key("s-5")),
        "<ln1> centimeter | <ln1> CM":
            R(Text("%(ln1)scm")),
        "<ln1> inch | <ln1> IN":
            R(Text("%(ln1)sin")),
        "<ln1> millimeter | <ln1> MM":
            R(Text("%(ln1)smm")),
        "<ln1> pica | <ln1> PC":
            R(Text("%(ln1)spc")),
        "<ln1> point | <ln1> PT":
            R(Text("%(ln1)spt")),
        "<ln1> CH":
            R(Text("%(ln1)sch")),
        "<ln1> EM":
            R(Text("%(ln1)sem")),
        "<ln1> EX":
            R(Text("%(ln1)sex")),
        "<ln1> REM":
            R(Text("%(ln1)srem")),
        "<ln1> viewport height | <ln1> VH":
            R(Text("%(ln1)svh")),
        "<ln1> viewport width | <ln1> VW":
            R(Text("%(ln1)svw")),
        "<ln1> millisecond | <ln1> MS":
            R(Text("%(ln1)sms")),
        "<ln1> second | <ln1> S":
            R(Text("%(ln1)ss")),
        #background
        "background image":
            R(Text("background-image:;") + Key("left/10:1")),
        "background position":
            R(Text("background-position:;") + Key("left/10:1")),
        "background size":
            R(Text("background-size:;") + Key("left/10:1")),
        "background repeat":
            R(Text("background-repeat:;") + Key("left/10:1")),
        "background attachment":
            R(Text("background-attachment:;") + Key("left/10:1")),
        "background origin":
            R(Text("background-origin:;") + Key("left/10:1")),
        "background clip":
            R(Text("background-clip:;") + Key("left/10:1")),
        "background color":
            R(Text("background-color:;") + Key("left/10:1")),
        "background attachment":
            R(Text("background-attachment:;") + Key("left/10:1")),
        "background origin":
            R(Text("background-origin:;") + Key("left/10:1")),
        "background clip":
            R(Text("background-clip:;") + Key("left/10:1")),
        #border
        "border":
            R(Text("border:;") + Key("left/10:1")),
        "border top":
            R(Text("border-top:;") + Key("left/10:1")),
        "border bottom":
            R(Text("border-bottom:;") + Key("left/10:1")),
        "border left":
            R(Text("border-left:;") + Key("left/10:1")),
        "border right":
            R(Text("border-right:;") + Key("left/10:1")),
        "border width":
            R(Text("border-width:;") + Key("left/10:1")),
        "border style":
            R(Text("border-style:;") + Key("left/10:1")),
        "border color":
            R(Text("border-color:;") + Key("left/10:1")),
        "border break":
            R(Text("border-break:;") + Key("left/10:1")),
        "border image":
            R(Text("border-image:;") + Key("left/10:1")),
        "border radius":
            R(Text("border-radius:;") + Key("left/10:1")),
        #box model
        "box shadow":
            R(Text("box-shadow:;") + Key("left/10:1")),
        "border-box":
            R(Text("border-box")),
        "height":
            R(Text("height:;") + Key("left/10:1")),
        "width":
            R(Text("width:;") + Key("left/10:1")),
        "min height":
            R(Text("min-height:;") + Key("left/10:1")),
        "max height":
            R(Text("max-height:;") + Key("left/10:1")),
        "min width":
            R(Text("min-width:;") + Key("left/10:1")),
        "max width":
            R(Text("max-width:;") + Key("left/10:1")),
        "padding box":
            R(Text("padding-box")),
        "content box":
            R(Text("content-box")),
        "margin":
            R(Text("margin:;") + Key("left/10:1")),
        "margin top":
            R(Text("margin-top:;") + Key("left/10:1")),
        "margin bottom":
            R(Text("margin-bottom:;") + Key("left/10:1")),
        "margin left":
            R(Text("margin-left:;") + Key("left/10:1")),
        "margin right":
            R(Text("margin-right:;") + Key("left/10:1")),
        "padding":
            R(Text("padding:;") + Key("left/10:1")),
        "padding top":
            R(Text("padding-top:;") + Key("left/10:1")),
        "padding bottom":
            R(Text("padding-bottom:;") + Key("left/10:1")),
        "padding left":
            R(Text("padding-left:;") + Key("left/10:1")),
        "padding right":
            R(Text("padding-right:;") + Key("left/10:1")),
        "display":
            R(Text("display:;") + Key("left/10:1")),
        "overflow":
            R(Text("overflow:;") + Key("left/10:1")),
        "overflow y":
            R(Text("overflow-y:;") + Key("left/10:1")),
        "overflow x":
            R(Text("overflow-x:;") + Key("left/10:1")),
        "overflow style":
            R(Text("overflow-style:;") + Key("left/10:1")),
        "visibility":
            R(Text("visibility:;") + Key("left/10:1")),
        "clear":
            R(Text("clear:;") + Key("left/10:1")),
        #Font
        "font":
            R(Text("font:;") + Key("left/10:1")),
        "font style":
            R(Text("font-style:;") + Key("left/10:1")),
        "font variant":
            R(Text("font-variant:;") + Key("left/10:1")),
        "font weight":
            R(Text("font-weight:;") + Key("left/10:1")),
        "font size":
            R(Text("font-size:;") + Key("left/10:1")),
        "font family":
            R(Text("font-family:;") + Key("left/10:1")),
        #text
        "direction":
            R(Text("direction:;") + Key("left/10:1")),
        "hanging punctuation":
            R(Text("hanging-punctuation:;") + Key("left/10:1")),
        "letter spacing":
            R(Text("letter-spacing:;") + Key("left/10:1")),
        "text outline":
            R(Text("text-outline:;") + Key("left/10:1")),
        "unicode bidi":
            R(Text("unicode-bidi:;") + Key("left/10:1")),
        "white space":
            R(Text("white-space:;") + Key("left/10:1")),
        "white space collapse":
            R(Text("white-space-collapse:;") + Key("left/10:1")),
        "punctuation trim":
            R(Text("punctuation-trim:;") + Key("left/10:1")),
        "text align":
            R(Text("text-align:;") + Key("left/10:1")),
        "text align last":
            R(Text("text-align-last:;") + Key("left/10:1")),
        "text decoration":
            R(Text("text-decoration:;") + Key("left/10:1")),
        "text shadow":
            R(Text("text-shadow:;") + Key("left/10:1")),
        "word break":
            R(Text("word-break:;") + Key("left/10:1")),
        "word wrap":
            R(Text("word-wrap:;") + Key("left/10:1")),
        "text emphasis":
            R(Text("text-emphasis:;") + Key("left/10:1")),
        "text indent":
            R(Text("text-indent:;") + Key("left/10:1")),
        "text justify":
            R(Text("text-justify:;") + Key("left/10:1")),
        "text transform":
            R(Text("text-transform:;") + Key("left/10:1")),
        "text wrap":
            R(Text("text-wrap:;") + Key("left/10:1")),
        "word spacing":
            R(Text("word-spacing:;") + Key("left/10:1")),
        #column
        "column count":
            R(Text("column-count:;") + Key("left/10:1")),
        "column fill":
            R(Text("column-fill:;") + Key("left/10:1")),
        "column gap":
            R(Text("column-gap:;") + Key("left/10:1")),
        "column rule":
            R(Text("column-rule:;") + Key("left/10:1")),
        "column rule style":
            R(Text("column-rule-style:;") + Key("left/10:1")),
        "column":
            R(Text("column:;") + Key("left/10:1")),
        "column rule width":
            R(Text("column-rule-width:;") + Key("left/10:1")),
        "column span":
            R(Text("column-span:;") + Key("left/10:1")),
        "column width":
            R(Text("column-width:;") + Key("left/10:1")),
        #colors
        "color":
            R(Text("color:;") + Key("left/10:1")),
        "opacity":
            R(Text("opacity:;") + Key("left/10:1")),
        #table
        "border collapse":
            R(Text("border-collapse:;") + Key("left/10:1")),
        "empty cells":
            R(Text("empty-cells:;") + Key("left/10:1")),
        "border spacing":
            R(Text("border-spacing:;") + Key("left/10:1")),
        "table layout":
            R(Text("table-layout:;") + Key("left/10:1")),
        "caption side":
            R(Text("caption-side:;") + Key("left/10:1")),
        #List & Markers
        "list style":
            R(Text("list-style:;") + Key("left/10:1")),
        "list style type":
            R(Text("list-style-type:;") + Key("left/10:1")),
        "list style position":
            R(Text("list-style-position:;") + Key("left/10:1")),
        "list style image":
            R(Text("list-style-image:;") + Key("left/10:1")),
        "marker offset":
            R(Text("marker-offset:;") + Key("left/10:1")),
        #Animations
        "animations":
            R(Text("animations:;") + Key("left/10:1")),
        "animation name":
            R(Text("animation-name:;") + Key("left/10:1")),
        "animation duration":
            R(Text("animation-duration:;") + Key("left/10:1")),
        "animation timing function":
            R(Text("animation-timing-function:;") + Key("left/10:1")),
        "animation delay":
            R(Text("animation-delay:;") + Key("left/10:1")),
        "animation iteration count":
            R(Text("animation-iteration-count:;") + Key("left/10:1")),
        "animation direction":
            R(Text("animation-direction:;") + Key("left/10:1")),
        "animation play state":
            R(Text("animation-play-state:;") + Key("left/10:1")),
        #Transitions
        "transitions":
            R(Text("transitions:;") + Key("left/10:1")),
        "transitions property":
            R(Text("transitions-property:;") + Key("left/10:1")),
        "transitions duration":
            R(Text("transitions-duration:;") + Key("left/10:1")),
        "transitions timing function":
            R(Text("transitions-timing-function:;") + Key("left/10:1")),
        "transitions delay":
            R(Text("transitions-delay:;") + Key("left/10:1")),
        "transitions property":
            R(Text("transitions-property:;") + Key("left/10:1")),
        #UI
        "webkit appearance | appearance":
            R(Text("-webkit-appearance:;") + Key("left/10:1")),
        "cursor":
            R(Text("cursor:;") + Key("left/10:1")),
        "resize":
            R(Text("resize:;") + Key("left/10:1")),
        #Pseudo-Class
        "active":
            R(Text(":active")),
        "focus":
            R(Text(":focus")),
        "hover":
            R(Text(":hover")),
        "link":
            R(Text(":link")),
        "disabled":
            R(Text(":disabled")),
        "enabled":
            R(Text(":enabled")),
        "checked":
            R(Text(":checked")),
        "selection":
            R(Text(":selection")),
        "lang":
            R(Text(":lang")),
        "nth child":
            R(Text(":nth-child()") + Key("left/10:1")),
        "nth last child":
            R(Text(":nth-last-child()") + Key("left/10:1")),
        "first child":
            R(Text(":first-child")),
        "last child":
            R(Text(":last-child")),
        "only-child":
            R(Text(":only-child")),
        "nth of type":
            R(Text(":nth-of-type()") + Key("left/10:1")),
        "nth last of type ":
            R(Text(":nth-last-of-type() ") + Key("left/10:1")),
        "last of type":
            R(Text(":last-of-type")),
        "first of type":
            R(Text(":first-of-type")),
        "only of type":
            R(Text(":only-of-type")),
        "empty":
            R(Text(":empty")),
        "root":
            R(Text(":root")),
        "not":
            R(Text(":not()") + Key("left/10:1")),
        "target":
            R(Text(":target")),
        "first letter":
            R(Text("::first-letter")),
        "first line":
            R(Text("::first-line")),
        "before":
            R(Text("::before")),
        "after":
            R(Text("::after")),
        #Outline
        "outline":
            R(Text("outline:;") + Key("left/10:1")),
        "outline color":
            R(Text("outline-color:;") + Key("left/10:1")),
        "outline style":
            R(Text("outline-style:;") + Key("left/10:1")),
        "outline width":
            R(Text("outline-width:;") + Key("left/10:1")),
        "outline offset":
            R(Text("outline-offset:;") + Key("left/10:1")),
        #transform
        "backface visibility":
            R(Text("backface-visibility:;") + Key("left/10:1")),
        "perspective":
            R(Text("perspective:;") + Key("left/10:1")),
        "perspective origin":
            R(Text("perspective-origin:;") + Key("left/10:1")),
        "transform":
            R(Text("transform:;") + Key("left/10:1")),
        "transform style":
            R(Text("transform-style:;") + Key("left/10:1")),
        #Positioning
        "position":
            R(Text("position:;") + Key("left/10:1")),
        "clip":
            R(Text("clip:;") + Key("left/10:1")),
        "z index":
            R(Text("z-index:;") + Key("left/10:1")),
        #flex
        "flex direction":
            R(Text("flex-direction:;") + Key("left/10:1")),
        "flex wrap":
            R(Text("flex-wrap:;") + Key("left/10:1")),
        "align items":
            R(Text("align-items:;") + Key("left/10:1")),
        "justify content":
            R(Text("justify-content:;") + Key("left/10:1")),
        "flex grow":
            R(Text("flex-grow:;") + Key("left/10:1")),
        "align self":
            R(Text("align-self:;") + Key("left/10:1")),
        "flex shrink":
            R(Text("flex-shrink:;") + Key("left/10:1")),
        "flex basis":
            R(Text("flex-basis:;") + Key("left/10:1")),
        "order":
            R(Text("order:;") + Key("left/10:1")),


        #values
        "url":
            R(Text("url()") + Key("left/10:1")),
        "rgb":
            R(Text("rgb(,,)") + Key("left/10:3")),
        "rgba":
            R(Text("rgba(,,,)") + Key("left/10:4")),
        

    }
    extras = [
        IntegerRefST("ln1", 1, 1000),
    ]
    defaults = {}

def get_rule():
    return CSS, RuleDetails(ccrtype=CCRType.GLOBAL)