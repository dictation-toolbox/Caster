
from castervoice.lib import control
from castervoice.lib.context import AppContext
from castervoice.lib.actions import Key
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib import settings

# HTML auto complete workaround for Jetbrains Products
# If more applications have issues with auto complete may be moved to actions.py
context = AppContext(executable=["idea", "idea64", "studio64", "pycharm", "webstorm64", "webstorm"])

if context:
    from dragonfly.actions.action_paste import Paste as Text
    if settings.SETTINGS["miscellaneous"]["use_aenea"]:
        try:
            from aenea import Paste as Text
        except ImportError:
            print("Unable to import aenea Paste actions. Dragonfly actions will be used "
            "instead.")
else: 
    from castervoice.lib.actions import Text

class HTML(MergeRule):
    mapping = {
        # A macro with ## is depreciated HTML.
        #Macros
        "make link":
            R(Text("<a href=''></a>") + Key("left/10:6"), rdescript="HTML: Make Link"),
        "table macro":
            R(Text("<table>") + Key("enter") + Text("<tr>") + Key("enter") +
            Text("<td></td>") + Key("enter") + Text("</tr>") + Key("enter") +
            Text("</table>"), rdescript="HTML: Table Macro"),
        "checkbox":
            R(Text("<input type=\"checkbox\">"), rdescript="HTML: Checkbox"),
        #HTML elements
        #Basic or Root elements
        "HTML":
            R(Text("<html>") + Key("enter") + Text("</html>") + Key("up"), rdescript="HTML: HTML"),
        "doc type":
            R(Text("<!DOCTYPE html>") + Key("enter"), rdescript="HTML: Doc Type"),
        #Document metadata
        "base":
            R(Text("<base >") + Key("left/10:1"), rdescript="HTML: Base"),
        "head":
            R(Text("<head>") + Key("enter") + Text("</head>") + Key("up"), rdescript="HTML: Head"),
        "link":
            R(Text("<link >") + Key("left/10:1"), rdescript="HTML: Link"),
        "meta":
            R(Text("<meta >") + Key("left/10:1"), rdescript="HTML: Meta"),
        "style":
            R(Text("<style >") + Key("left/10:1"), rdescript="HTML: Style"),
        "style close":
            R(Text("</style>"), rdescript="HTML: Style Close"),
        "title":
            R(Text("<title></title>") + Key("left/10:8"), rdescript="HTML: Title"),
        #Content sectioning
        "address ":
            R(Text("<address>") + Key("enter") + Text("</address>") + Key("up"), rdescript="HTML: Address"),
        "article ":
            R(Text("<article >"), rdescript="HTML: Article"),
        "close article":
            R(Text("</article>"), rdescript="HTML: Close Article"),
        "body":
            R(Text("<body>") + Key("enter") + Text("</body>") + Key("up"), rdescript="HTML: Body"),
        "footer":
            R(Text("<footer>") + Key("enter") + Text("</footer>") + Key("up"), rdescript="HTML: Footer"),
        "header":
            R(Text("<header>") + Key("enter") + Text("</header>") + Key("up"), rdescript="HTML: Header"),
        "H 1 | heading one":
            R(Text("<h1></h1>") + Key("left/10:5"), rdescript="HTML: Heading 1"),
        "H 2 | heading to":
            R(Text("<h2></h2>") + Key("left/10:5"), rdescript="HTML: Heading 2"),
        "H 3 | heading three":
            R(Text("<h3></h3>") + Key("left/10:5"), rdescript="HTML: Heading 3"),
        "H 4 | heading for":
            R(Text("<h4></h4>") + Key("left/10:5"), rdescript="HTML: Heading 4"),
        "H 5 | heading five":
            R(Text("<h5></h5>") + Key("left/10:5"), rdescript="HTML: Heading 5"),
        "H 6 | heading six":
            R(Text("<h6></h6>") + Key("left/10:5"), rdescript="HTML: Heading 6"),
        "H group | headings group":
            R(Text("<hgroup></hgroup>") + Key("left/10:9"), rdescript="HTML: Group"),
        "navigation | navigate":
            R(Text("<nav>") + Key("enter") + Text("</nav>") + Key("up"), rdescript="HTML: Navigate"),
        "section":
            R(Text("<section>") + Key("enter") + Text("</section>") + Key("up"), rdescript="HTML: Section"),
        # Text content
        "description | DD":
            R(Text("<dd>"), rdescript="HTML: Description"),
        "division":
            R(Text("<div></div>") + Key("left/10:6"), rdescript="HTML: Division"),
        "list element | DL":
            R(Text("<dl>"), rdescript="HTML: List Element"),
        "fig caption":
            R(Text("<figcaption>"), rdescript="HTML: Fig Caption"),
        "figure":
            R(Text("<figure>"), rdescript="HTML: Figure"),
        "H are | HR":
            R(Text("<hr>"), rdescript="HTML: HR"),
        "list item | LI":
            R(Text("<li></li>") + Key("left/10:5"), rdescript="HTML: List Item"),
        "main":
            R(Text("<main>") + Key("enter") + Text("</main>") + Key("up"), rdescript="HTML: Main"),
        "ordered list | OL":
            R(Text("<ol>") + Key("enter") + Text("</ol>") + Key("up"), rdescript="HTML: Ordered List"),
        "paragraph":
            R(Text("<p>") + Key("enter") + Text("</p>") + Key("up"), rdescript="HTML: Paragraph"),
        "pre-format":
            R(Text("<pre>") + Key("enter") + Text("</pre>") + Key("up"), rdescript="HTML: Pre-format"),
        "unordered list | UL":
            R(Text("<ul>") + Key("enter") + Text("</ul>") + Key("up"), rdescript="HTML: Unordered List"),
        #Inline text semantics
        "anchor":
            R(Text("<a></a>") + Key("left/10:4"), rdescript="HTML: Anchor"),
        "abbreviation":
            R(Text("<abbr></abbr>") + Key("left/10:7"), rdescript="HTML: Abbreviation"),
        "bold":
            R(Text("<b></b>") + Key("left/10:4"), rdescript="HTML: Bold"),
        "override":
            R(Text("<bdo></bdo>") + Key("left/10:6"), rdescript="HTML: Override"),
        "isolate | bi-directional isolation":
            R(Text("<bdi></bdi>") + Key("left/10:6"), rdescript="HTML: Bi-directional Isolation"),
        "break | be are | BR":
            R(Text("<br>") + Key("enter"), rdescript="HTML: Break"),
        "code":
            R(Text("<code></code>") + Key("left/10:7"), rdescript="HTML: Code"),
        "data":
            R(Text("<data></data>") + Key("left/10:7"), rdescript="HTML: Data"),
        "defining instance":
            R(Text("<dfn></dfn>") + Key("left/10:6"), rdescript="HTML: Defining Instance"),
        "emphasis | EM":
            R(Text("<em></em>") + Key("left/10:5"), rdescript="HTML: Emphasis"),
        "semantics | italics":
            R(Text("<i></i>") + Key("left/10:4"), rdescript="HTML: Semantics | Italics"),
        "keyboard input":
            R(Text("<kbd></kbd>") + Key("left/10:6"), rdescript="HTML: Keyboard Input"),
        "mark | highlight":
            R(Text("<mark></mark>") + Key("left/10:7"), rdescript="HTML: Mark | Highlight"),
        "quote":
            R(Text("<q></q>") + Key("left/10:4"), rdescript="HTML: Quote"),
        "fall-back parenthesis | RP":
            R(Text("<rp></rp>") + Key("left/10:5"), rdescript="HTML: Fall-back Parentheses"),
        "embraces pronunciation | RT":
            R(Text("<rt></rt>") + Key("left/10:5"), rdescript="HTML: Embrace Pronunciation"),
        "ruby | pronounce asian":
            R(Text("<ruby></ruby>") + Key("left/10:7"), rdescript="HTML: Ruby | Pronounce Asian"),
        ##"strike through | strike":    Text("<s></s>")+  Key("left/10:4"), rdescript="HTML: Strike Through | Strike"),
        "deleted text | deleted | replaced":
            R(Text("<del></del>") + Key("left/10:6"), rdescript="HTML: Deleted Text | Deleted | Replaced"),
        "sample output":
            R(Text("<samp></samp>") + Key("left/10:7"), rdescript="HTML: Sample Output"),
        "small":
            R(Text("<small></small>") + Key("left/10:8"), rdescript="HTML: Small"),
        "span":
            R(Text("<span></span>") + Key("left/10:7"), rdescript="HTML: Span"),
        "strong":
            R(Text("<strong></strong>") + Key("left/10:9"), rdescript="HTML: Strong"),
        "subscript":
            R(Text("<sub></sub>") + Key("left/10:6"), rdescript="HTML: Subscript"),
        "superscript":
            R(Text("<sup></sup>") + Key("left/10:6"), rdescript="HTML: Superscript"),
        "time":
            R(Text("<time></time>") + Key("left/10:7"), rdescript="HTML: Time"),
        "underline":
            R(Text("<u></u>") + Key("left/10:4"), rdescript="HTML: Underline"),
        "variable":
            R(Text("<var></var>") + Key("left/10:6"), rdescript="HTML: Variable"),
        "optional break":
            R(Text("<wbr></wbr>") + Key("left/10:6"), rdescript="HTML: Optional Break"),
        #Image & multimedia
        "area":
            R(Text("<area />") + Key("left/10:2"), rdescript="HTML: Area"),
        "audio":
            R(Text("<audio>") + Key("enter") + Text("</audio>") + Key("up"), rdescript="HTML: Audio"),
        "image ":
            R(Text("<img></img>") + Key("left/10:6"), rdescript="HTML: Image"),
        "map":
            R(Text("<map>") + Key("enter") + Text("</map>") + Key("up"), rdescript="HTML: Map"),
        "track":
            R(Text("<track >") + Key("left/10:1"), rdescript="HTML: Track"),
        "video":
            R(Text("<video >") + Key("left/10:1"), rdescript="HTML: Video"),
        "video close":
            R(Text("</video>"), rdescript="HTML: Video Close"),
        #embedded content
        "embedded":
            R(Text("<embed >") + Key("left/10:1"), rdescript="HTML: Embedded"),
        "inline frame":
            R(Text("<iframe >") + Key("left/10:1"), rdescript="HTML: Inline Frame"),
        "inline frame close":
            R(Text("</iframe>") + Key("left/10:1"), rdescript="HTML: In-line Frame Close"),
        "object | embedded object":
            R(Text("<object >") + Key("left/10:1"), rdescript="HTML: Object | Embedded Object"),
        "parameter ":
            R(Text("<param >") + Key("left/10:1"), rdescript="HTML: Parameter"),
        "source":
            R(Text("<source >") + Key("left/10:1"), rdescript="HTML: Source"),
        #Scripting
        "canvas":
            R(Text("<canvas >") + Key("left/10:1"), rdescript="HTML: Canvas"),
        "canvas close":
            R(Text("</canvas>"), rdescript="HTML: Canvas Close"),
        "noscript":
            R(Text("<noscript>") + Key("enter") + Text("</noscript>") + Key("up"), rdescript="HTML: NoScript"),
        "script":
            R(Text("<script></script>") + Key("left/10:9"), rdescript="HTML: Script"),
        #Edits
        "inserted text | inserted":
            R(Text("<ins></ins>") + Key("left/10:6"), rdescript="HTML: Inserted Text | Inserted"),
        #Table content
        "table caption | tee caption":
            R(Text("<caption>"), rdescript="HTML: Table Caption"),
        "table column | tee column":
            R(Text("<col>"), rdescript="HTML: Table Column"),
        "table column group | tee group":
            R(Text("<colgroup>"), rdescript="HTML: Table Column Group"),
        "table":
            R(Text("<table>"), rdescript="HTML: Table"),
        "table body":
            R(Text("<tbody>"), rdescript="HTML: Table Body"),
        "table cell | TD | tee D":
            R(Text("<td></td>") + Key("left/10:5"), rdescript="HTML: Table Body Cell"),
        "table foot":
            R(Text("<tfoot>"), rdescript="HTML: Table Foot"),
        "table header | TH":
            R(Text("<th>"), rdescript="HTML: Table Header"),
        "table head | thead":
            R(Text("<thead>"), rdescript="HTML: Table Head"),
        "table row | tee are":
            R(Text("<tr></tr>") + Key("left/10:5"), rdescript="HTML: Table Row"),
        #Forms
        "button":
            R(Text("<button></button>") + Key("left/10:9"), rdescript="HTML: Button"),
        "data list":
            R(Text("<datalist>") + Key("enter") + Text("</datalist>") + Key("up"), rdescript="HTML: Data List"),
        "field set":
            R(Text("<fieldset>") + Key("enter") + Text("</fieldset>") + Key("up"), rdescript="HTML: Field Set"),
        "field set close":
            R(Text("</fieldset>"), rdescript="HTML: Field Set Close"),
        "form":
            R(Text("<form>") + Key("enter") + Text("</form>") + Key("up"), rdescript="HTML: Form"),
        "input":
            R(Text("<input >") + Key("left/10:1"), rdescript="HTML: Input"),
        "keygen":
            R(Text("<keygen >") + Key("left/10:1"), rdescript="HTML: Keygen"),
        "label":
            R(Text("<label>"), rdescript="HTML: Label"),
        "label close":
            R(Text("</label>"), rdescript="HTML: Label Close"),
        "legend":
            R(Text("<legend>"), rdescript="HTML: Legend"),
        "meter":
            R(Text("<meter >") + Key("left/10:1"), rdescript="HTML: Meter"),
        "meter close":
            R(Text("</meter>"), rdescript="HTML: Meter Close"),
        "opt group":
            R(Text("<optgroup>") + Key("enter") + Text("</optgroup>") + Key("up"), rdescript="HTML: Opt Group"),
        "option":
            R(Text("<option >") + Key("left/10:1"), rdescript="HTML: Option"),
        "option close":
            R(Text("</option>"), rdescript="HTML: Option Close"),
        "output":
            R(Text("<output >") + Key("left/10:1"), rdescript="HTML: Output"),
        "output close":
            R(Text("</output>"), rdescript="HTML: Output Close"),
        "progress":
            R(Text("<progress >") + Key("left/10:1"), rdescript="HTML: Progress"),
        "select":
            R(Text("<select>") + Key("enter") + Text("</select>") + Key("up"), rdescript="HTML: Select"),
        "text area":
            R(Text("<textarea >") + Key("left/10:1"), rdescript="HTML: Text Area"),
        "text area close":
            R(Text("</textarea>"), rdescript="HTML: Text Area Close"),
        #Interactive elements
        "details":
            R(Text("<details>"), rdescript="HTML: Details"),
        "dialog":
            R(Text("<dialog>"), rdescript="HTML: Dialogue"),
        "menu":
            R(Text("<menu>"), rdescript="HTML: Menu"),
        "menu item":
            R(Text("<menuitem>"), rdescript="HTML: Menu Item"),
        "summary":
            R(Text("<summary>"), rdescript="HTML: Summary"),
        #Web Components: As defined in (W3C)
        "content":
            R(Text("<content>"), rdescript="HTML: Context"),
        "decorator":
            R(Text("<decorator>"), rdescript="HTML: Decorator"),
        "element":
            R(Text("<element>"), rdescript="HTML: Element"),
        "shadow":
            R(Text("<shadow>"), rdescript="HTML: Shadow"),
        "template":
            R(Text("<template>"), rdescript="HTML: Template"),
    }
    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(HTML())
