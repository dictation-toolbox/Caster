from dragonfly import Key, Text

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule


class HTML(MergeRule):
    mapping = {
        # A macro with ## is depreciated HTML.
        #Macros
        "make link":
            Text("<a href=''></a>") + Key("left/10:6"),
        "table macro":
            Text("<table>") + Key("enter") + Text("<tr>") + Key("enter") +
            Text("<td></td>") + Key("enter") + Text("</tr>") + Key("enter") +
            Text("</table>"),
        "close tag":
            Key("c-left/10:2"),
        "checkbox":
            Text("<input type=\"checkbox\">"),

        #HTML elements
        #Basic or Root elements
        "HTML":
            Text("<html>") + Key("enter") + Text("</html>") + Key("up"),
        "DOC TYPE":
            Text("<!DOCTYPE html>") + Key("enter"),
        #Document metadata
        "base":
            Text("<base >") + Key("left/10:1"),
        "head":
            Text("<head>") + Key("enter") + Text("</head>") + Key("up"),
        "link":
            Text("<link >") + Key("left/10:1"),
        "meta":
            Text("<meta >") + Key("left/10:1"),
        "style":
            Text("<style >") + Key("left/10:1"),
        "style close":
            Text("</style>"),
        "title":
            Text("<title></title>") + Key("left/10:8"),
        #Content sectioning
        "address ":
            Text("<address>") + Key("enter") + Text("</address>") + Key("up"),
        "article ":
            Text("<article >"),
        "close article":
            Text("</article>"),
        "body":
            Text("<body>") + Key("enter") + Text("</body>") + Key("up"),
        "footer":
            Text("<footer>") + Key("enter") + Text("</footer>") + Key("up"),
        "header":
            Text("<header>") + Key("enter") + Text("</header>") + Key("up"),
        "H 1 | heading one":
            Text("<h1></h1>") + Key("left/10:5"),
        "H 2 | heading to":
            Text("<h2></h2>") + Key("left/10:5"),
        "H 3 | heading three":
            Text("<h3></h3>") + Key("left/10:5"),
        "H 4 | heading for":
            Text("<h4></h4>") + Key("left/10:5"),
        "H 5 | heading five":
            Text("<h5></h5>") + Key("left/10:5"),
        "H 6 | heading six":
            Text("<h6></h6>") + Key("left/10:5"),
        "H group | headings group":
            Text("<hgroup></hgroup>") + Key("left/10:9"),
        "navigation | navigate":
            Text("<nav>") + Key("enter") + Text("</nav>") + Key("up"),
        "section":
            Text("<section>") + Key("enter") + Text("</section>") + Key("up"),
        #Text content
        "description | DD":
            Text("<dd>"),
        "division":
            Text("<div></div>") + Key("left/10:6"),
        "list element | DL":
            Text("<dl>"),
        "fig caption":
            Text("<figcaption>"),
        "figure":
            Text("<figure>"),
        "H are | HR":
            Text("<hr>"),
        "list item | LI":
            Text("<li></li>") + Key("left/10:5"),
        "main":
            Text("<main>") + Key("enter") + Text("</main>") + Key("up"),
        "ordered list | OL":
            Text("<ol>") + Key("enter") + Text("</ol>") + Key("up"),
        "paragraph":
            Text("<p>") + Key("enter") + Text("</p>") + Key("up"),
        "pre-format":
            Text("<pre>") + Key("enter") + Text("</pre>") + Key("up"),
        "unordered list | UL":
            Text("<ul>") + Key("enter") + Text("</ul>") + Key("up"),
        #Inline text semantics
        "anchor":
            Text("<a></a>") + Key("left/10:4"),
        "abbreviation":
            Text("<abbr></abbr>") + Key("left/10:7"),
        "bold":
            Text("<b></b>") + Key("left/10:4"),
        "override":
            Text("<bdo></bdo>") + Key("left/10:6"),
        "isolate | bi-directional isolation":
            Text("<bdi></bdi>") + Key("left/10:6"),
        "break | be are | BR":
            Text("<br>") + Key("enter"),
        "code":
            Text("<code></code>") + Key("left/10:7"),
        "data":
            Text("<data></data>") + Key("left/10:7"),
        "defining instance":
            Text("<dfn></dfn>") + Key("left/10:6"),
        "emphasis | EM":
            Text("<em></em>") + Key("left/10:5"),
        "semantics | italics":
            Text("<i></i>") + Key("left/10:4"),
        "keyboard input":
            Text("<kbd></kbd>") + Key("left/10:6"),
        "mark | highlight":
            Text("<mark></mark>") + Key("left/10:7"),
        "quote":
            Text("<q></q>") + Key("left/10:4"),
        "fall-back parenthesis | RP":
            Text("<rp></rp>") + Key("left/10:5"),
        "embraces pronunciation | RT":
            Text("<rt></rt>") + Key("left/10:5"),
        "ruby | pronounce asian":
            Text("<ruby></ruby>") + Key("left/10:7"),
        ##"strike through | strike":    Text("<s></s>")+  Key("left/10:4"),
        "deleted text | deleted | replaced":
            Text("<del></del>") + Key("left/10:6"),
        "sample output":
            Text("<samp></samp>") + Key("left/10:7"),
        "small":
            Text("<small></small>") + Key("left/10:8"),
        "span":
            Text("<span></span>") + Key("left/10:7"),
        "strong":
            Text("<strong></strong>") + Key("left/10:9"),
        "subscript":
            Text("<sub></sub>") + Key("left/10:6"),
        "superscript":
            Text("<sup></sup>") + Key("left/10:6"),
        "time":
            Text("<time></time>") + Key("left/10:7"),
        "underline":
            Text("<u></u>") + Key("left/10:4"),
        "variable":
            Text("<var></var>") + Key("left/10:6"),
        "optional break":
            Text("<wbr></wbr>") + Key("left/10:6"),
        #Image & multimedia
        "area":
            Text("<area />") + Key("left/10:2"),
        "audio":
            Text("<audio>") + Key("enter") + Text("</audio>") + Key("up"),
        "image ":
            Text("<img></img>") + Key("left/10:6"),
        "map":
            Text("<map>") + Key("enter") + Text("</map>") + Key("up"),
        "track":
            Text("<track >") + Key("left/10:1"),
        "video":
            Text("<video >") + Key("left/10:1"),
        "video close":
            Text("</video>"),
        #embedded content
        "embedded":
            Text("<embed >") + Key("left/10:1"),
        "inline frame":
            Text("<iframe >") + Key("left/10:1"),
        "inline frame close":
            Text("</iframe>") + Key("left/10:1"),
        "object| embedded object":
            Text("<object >") + Key("left/10:1"),
        "parameter ":
            Text("<param >") + Key("left/10:1"),
        "source":
            Text("<source >") + Key("left/10:1"),
        #Scripting
        "canvas":
            Text("<canvas >") + Key("left/10:1"),
        "canvas close":
            Text("</canvas>"),
        "noscript":
            Text("<noscript>") + Key("enter") + Text("</noscript>") + Key("up"),
        "script":
            Text("<script></script>") + Key("left/10:9"),
        #Edits
        "inserted text | inserted":
            Text("<ins></ins>") + Key("left/10:6"),
        #Table content
        "table caption | tee caption":
            Text("<caption>"),
        "table column | tee column":
            Text("<col>"),
        "table column group | tee group":
            Text("<colgroup>"),
        "table":
            Text("<table>"),
        "table body":
            Text("<tbody>"),
        "table cell | TD | tee D":
            Text("<td></td>") + Key("left/10:5"),
        "table foot":
            Text("<tfoot>"),
        "table header | TH":
            Text("<th>"),
        "table head | thead":
            Text("<thead>"),
        "table row | tee are":
            Text("<tr></tr>") + Key("left/10:5"),
        #Forms
        "button":
            Text("<button></button>") + Key("left/10:9"),
        "data list":
            Text("<datalist>") + Key("enter") + Text("</datalist>") + Key("up"),
        "field set":
            Text("<fieldset>") + Key("enter") + Text("</fieldset>") + Key("up"),
        "field set close":
            Text("</fieldset>"),
        "form":
            Text("<form>") + Key("enter") + Text("</form>") + Key("up"),
        "input":
            Text("<input >") + Key("left/10:1"),
        "keygen":
            Text("<keygen >") + Key("left/10:1"),
        "label":
            Text("<label>"),
        "label close":
            Text("</label>"),
        "legend":
            Text("<legend>"),
        "meter":
            Text("<meter >") + Key("left/10:1"),
        "meter close":
            Text("</meter>"),
        "opt group":
            Text("<optgroup>") + Key("enter") + Text("</optgroup>") + Key("up"),
        "option":
            Text("<option >") + Key("left/10:1"),
        "option close":
            Text("</option>"),
        "output":
            Text("<output >") + Key("left/10:1"),
        "output close":
            Text("</output>"),
        "progress":
            Text("<progress >") + Key("left/10:1"),
        "select":
            Text("<select>") + Key("enter") + Text("</select>") + Key("up"),
        "text area":
            Text("<textarea >") + Key("left/10:1"),
        "text area close":
            Text("</textarea>"),
        #Interactive elements
        "details":
            Text("<details>"),
        "dialog":
            Text("<dialog>"),
        "menu":
            Text("<menu>"),
        "menu item":
            Text("<menuitem>"),
        "summary":
            Text("<summary>"),
        #Web Components: As defined in (W3C)
        "content":
            Text("<content>"),
        "decorator":
            Text("<decorator>"),
        "element":
            Text("<element>"),
        "shadow":
            Text("<shadow>"),
        "template":
            Text("<template>"),
    }
    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(HTML())
