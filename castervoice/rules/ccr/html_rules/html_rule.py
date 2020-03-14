from castervoice.lib.actions import Key
from castervoice.lib import settings, printer
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.context import AppContext

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


class HTML(MergeRule):
    pronunciation = "html"

    mapping = {
        # A macro with ## is depreciated HTML.
        #Macros
        "make link":
            R(Text("<a href=''></a>") + Key("left/10:6")),
        "table macro":
            R(
                Text("<table>") + Key("enter") + Text("<tr>") + Key("enter") +
                Text("<td></td>") + Key("enter") + Text("</tr>") + Key("enter") +
                Text("</table>")),
        "check box":
            R(Text("<input type=\"checkbox\">")),
        #HTML elements
        #Basic or Root elements
        "HTML":
            R(Text("<html>") + Key("enter") + Text("</html>") + Key("up")),
        "doc type":
            R(Text("<!DOCTYPE html>") + Key("enter")),
        #Document metadata
        "base":
            R(Text("<base >") + Key("left/10:1")),
        "head":
            R(Text("<head>") + Key("enter") + Text("</head>") + Key("up")),
        "link":
            R(Text("<link >") + Key("left/10:1")),
        "meta":
            R(Text("<meta >") + Key("left/10:1")),
        "style":
            R(Text("<style >") + Key("left/10:1")),
        "style close":
            R(Text("</style>")),
        "title":
            R(Text("<title></title>") + Key("left/10:8")),
        #Content sectioning
        "address ":
            R(Text("<address>") + Key("enter") + Text("</address>") + Key("up")),
        "article ":
            R(Text("<article >")),
        "close article":
            R(Text("</article>")),
        "body":
            R(Text("<body>") + Key("enter") + Text("</body>") + Key("up")),
        "footer":
            R(Text("<footer>") + Key("enter") + Text("</footer>") + Key("up")),
        "header":
            R(Text("<header>") + Key("enter") + Text("</header>") + Key("up")),
        "H 1 | heading one":
            R(Text("<h1></h1>") + Key("left/10:5")),
        "H 2 | heading to":
            R(Text("<h2></h2>") + Key("left/10:5")),
        "H 3 | heading three":
            R(Text("<h3></h3>") + Key("left/10:5")),
        "H 4 | heading for":
            R(Text("<h4></h4>") + Key("left/10:5")),
        "H 5 | heading five":
            R(Text("<h5></h5>") + Key("left/10:5")),
        "H 6 | heading six":
            R(Text("<h6></h6>") + Key("left/10:5")),
        "H group | headings group":
            R(Text("<hgroup></hgroup>") + Key("left/10:9")),
        "navigation | navigate":
            R(Text("<nav>") + Key("enter") + Text("</nav>") + Key("up")),
        "section":
            R(Text("<section>") + Key("enter") + Text("</section>") + Key("up")),
        # Text content
        "description | DD":
            R(Text("<dd>")),
        "division":
            R(Text("<div></div>") + Key("left/10:6")),
        "list element | DL":
            R(Text("<dl>")),
        "fig caption":
            R(Text("<figcaption>")),
        "figure":
            R(Text("<figure>")),
        "H are | HR":
            R(Text("<hr>")),
        "list item | LI":
            R(Text("<li></li>") + Key("left/10:5")),
        "main":
            R(Text("<main>") + Key("enter") + Text("</main>") + Key("up")),
        "ordered list | OL":
            R(Text("<ol>") + Key("enter") + Text("</ol>") + Key("up")),
        "paragraph":
            R(Text("<p>") + Key("enter") + Text("</p>") + Key("up")),
        "pre format":
            R(Text("<pre>") + Key("enter") + Text("</pre>") + Key("up")),
        "unordered list | UL":
            R(Text("<ul>") + Key("enter") + Text("</ul>") + Key("up")),
        #Inline text semantics
        "anchor":
            R(Text("<a></a>") + Key("left/10:4")),
        "abbreviation":
            R(Text("<abbr></abbr>") + Key("left/10:7")),
        "bold":
            R(Text("<b></b>") + Key("left/10:4")),
        "override":
            R(Text("<bdo></bdo>") + Key("left/10:6")),
        "isolate | bi directional isolation":
            R(Text("<bdi></bdi>") + Key("left/10:6")),
        "break | be are | BR":
            R(Text("<br>") + Key("enter")),
        "code":
            R(Text("<code></code>") + Key("left/10:7")),
        "data":
            R(Text("<data></data>") + Key("left/10:7")),
        "defining instance":
            R(Text("<dfn></dfn>") + Key("left/10:6")),
        "emphasis | EM":
            R(Text("<em></em>") + Key("left/10:5")),
        "semantics | italics":
            R(Text("<i></i>") + Key("left/10:4")),
        "keyboard input":
            R(Text("<kbd></kbd>") + Key("left/10:6")),
        "mark | highlight":
            R(Text("<mark></mark>") + Key("left/10:7")),
        "quote":
            R(Text("<q></q>") + Key("left/10:4")),
        "fall back parenthesis | RP":
            R(Text("<rp></rp>") + Key("left/10:5")),
        "embraces pronunciation | RT":
            R(Text("<rt></rt>") + Key("left/10:5")),
        "ruby | pronounce asian":
            R(Text("<ruby></ruby>") + Key("left/10:7")),
        ##"strike through | strike":    Text("<s></s>")+  Key("left/10:4")),
        "deleted text | deleted | replaced":
            R(Text("<del></del>") + Key("left/10:6")),
        "sample output":
            R(Text("<samp></samp>") + Key("left/10:7")),
        "small":
            R(Text("<small></small>") + Key("left/10:8")),
        "span":
            R(Text("<span></span>") + Key("left/10:7")),
        "strong":
            R(Text("<strong></strong>") + Key("left/10:9")),
        "subscript":
            R(Text("<sub></sub>") + Key("left/10:6")),
        "super script":
            R(Text("<sup></sup>") + Key("left/10:6")),
        "time":
            R(Text("<time></time>") + Key("left/10:7")),
        "underline":
            R(Text("<u></u>") + Key("left/10:4")),
        "variable":
            R(Text("<var></var>") + Key("left/10:6")),
        "optional break":
            R(Text("<wbr></wbr>") + Key("left/10:6")),
        #Image & multimedia
        "area":
            R(Text("<area />") + Key("left/10:2")),
        "audio":
            R(Text("<audio>") + Key("enter") + Text("</audio>") + Key("up")),
        "image ":
            R(Text("<img></img>") + Key("left/10:6")),
        "map":
            R(Text("<map>") + Key("enter") + Text("</map>") + Key("up")),
        "track":
            R(Text("<track >") + Key("left/10:1")),
        "video":
            R(Text("<video >") + Key("left/10:1")),
        "video close":
            R(Text("</video>")),
        #embedded content
        "embedded":
            R(Text("<embed >") + Key("left/10:1")),
        "inline frame":
            R(Text("<iframe >") + Key("left/10:1")),
        "inline frame close":
            R(Text("</iframe>") + Key("left/10:1")),
        "object | embedded object":
            R(Text("<object >") + Key("left/10:1")),
        "parameter ":
            R(Text("<param >") + Key("left/10:1")),
        "source":
            R(Text("<source >") + Key("left/10:1")),
        #Scripting
        "canvas":
            R(Text("<canvas >") + Key("left/10:1")),
        "canvas close":
            R(Text("</canvas>")),
        "noscript":
            R(Text("<noscript>") + Key("enter") + Text("</noscript>") + Key("up")),
        "script":
            R(Text("<script></script>") + Key("left/10:9")),
        #Edits
        "inserted text | inserted":
            R(Text("<ins></ins>") + Key("left/10:6")),
        #Table content
        "table caption | tee caption":
            R(Text("<caption>")),
        "table column | tee column":
            R(Text("<col>")),
        "table column group | tee group":
            R(Text("<colgroup>")),
        "table":
            R(Text("<table>")),
        "table body":
            R(Text("<tbody>")),
        "table cell | TD | tee D":
            R(Text("<td></td>") + Key("left/10:5")),
        "table foot":
            R(Text("<tfoot>")),
        "table header | TH":
            R(Text("<th>")),
        "table head | thead":
            R(Text("<thead>")),
        "table row | tee are":
            R(Text("<tr></tr>") + Key("left/10:5")),
        #Forms
        "button":
            R(Text("<button></button>") + Key("left/10:9")),
        "data list":
            R(Text("<datalist>") + Key("enter") + Text("</datalist>") + Key("up")),
        "field set":
            R(Text("<fieldset>") + Key("enter") + Text("</fieldset>") + Key("up")),
        "field set close":
            R(Text("</fieldset>")),
        "form":
            R(Text("<form>") + Key("enter") + Text("</form>") + Key("up")),
        "input":
            R(Text("<input >") + Key("left/10:1")),
        "key gen":
            R(Text("<keygen >") + Key("left/10:1")),
        "label":
            R(Text("<label>")),
        "label close":
            R(Text("</label>")),
        "legend":
            R(Text("<legend>")),
        "meter":
            R(Text("<meter >") + Key("left/10:1")),
        "meter close":
            R(Text("</meter>")),
        "opt group":
            R(Text("<optgroup>") + Key("enter") + Text("</optgroup>") + Key("up")),
        "option":
            R(Text("<option >") + Key("left/10:1")),
        "option close":
            R(Text("</option>")),
        "output":
            R(Text("<output >") + Key("left/10:1")),
        "output close":
            R(Text("</output>")),
        "progress":
            R(Text("<progress >") + Key("left/10:1")),
        "select":
            R(Text("<select>") + Key("enter") + Text("</select>") + Key("up")),
        "text area":
            R(Text("<textarea >") + Key("left/10:1")),
        "text area close":
            R(Text("</textarea>")),
        #Interactive elements
        "details":
            R(Text("<details>")),
        "dialog":
            R(Text("<dialog>")),
        "menu":
            R(Text("<menu>")),
        "menu item":
            R(Text("<menuitem>")),
        "summary":
            R(Text("<summary>")),
        #Web Components: As defined in (W3C)
        "content":
            R(Text("<content>")),
        "decorator":
            R(Text("<decorator>")),
        "element":
            R(Text("<element>")),
        "shadow":
            R(Text("<shadow>")),
        "template":
            R(Text("<template>")),
    }
    extras = []
    defaults = {}


def get_rule():
    return HTML, RuleDetails(ccrtype=CCRType.GLOBAL)
