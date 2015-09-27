from dragonfly import Key, Text, Paste, MappingRule

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


class JavaNon(MappingRule):
    mapping = {
        "try catch":                        R(Text("try{}catch(Exception e){}"), rdescript="Java: Try Catch"),
        "deco override":                    R(Text("@Override"), rdescript="Java: Override Decorator"),
        "iterate and remove":               R(Paste("for (Iterator<TYPE> iterator = NAME.iterator(); iterator.hasNext();) {\n\tString string = iterator.next();\nif (CONDITION) {\niterator.remove();\n}\n}"), rdescript="Java: Iterate And Remove"),
        "string builder":                   R(Paste("StringBuilder builder = new StringBuilder(); builder.append(orgStr); builder.deleteCharAt(orgStr.length()-1);"), rdescript="Java: String Builder"),
          }

    ncextras   = []
    ncdefaults = {}

class Java(MergeRule):
    auto = [".java"]
    non = JavaNon
        
    mapping = {
        # CCR PROGRAMMING STANDARD
        "iffae":                            R(Text("if() {")+Key("enter,up,left"), rdescript="Java: If"),
        "shells":                           R(Text("else {")+Key("enter"), rdescript="Java: Else"),        
        #
        "switch":                           R(Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"), rdescript="Java: Switch"),
        "case of":                          R(Text("case :")+Key("left"), rdescript="Java: Case"),
        "breaker":                          R(Text("break;"), rdescript="Java: Break"),
        "default":                          R(Text("default: "), rdescript="Java: Default"),
        #
        "do loop":                          R(Text("do {}")+Key("left, enter:2"), rdescript="Java: Do Loop"),
        "while loop":                       R(Text("while ()")+Key("left"), rdescript="Java: While"),
        "for loop":                         R(Text("for (int i=0; i<VALUE; i++)"), rdescript="Java: For i Loop"),
        "for each":                         R(Text("for (CLASS TYPE : LIST)"), rdescript="Java: For Each Loop"),
        #
        "convert to integer":               R(Text("Integer.parseInt()")+ Key("left"), rdescript="Java: Convert To Integer"),
        "convert to floating point":        R(Text("Double.parseDouble()")+ Key("left"), rdescript="Java: Convert To Floating-Point"),
        "convert to string":                R(Key("dquote, dquote, plus"), rdescript="Java: Convert To String"),
        #
        "lodge and":                        R(Text(" && "), rdescript="Java: And"),
        "lodge or":                         R(Text(" || "), rdescript="Java: Or"),
        "lodge not":                        R(Text("!"), rdescript="Java: Not"),
        #
        "print to console":                 R(Text("java.lang.System.out.println()")+Key("left"), rdescript="Java: Print"),
        #
        "import":                           R(Text( "import " ), rdescript="Java: Import"),
        #
        "function":                         R(Text("SCOPE TYPE NAME(){}")+Key("left"), rdescript="Java: Function"),
        "class":                            R(Text("class {}")+Key("left/5:2"), rdescript=""),
        
        #
        "add comment":                      R(Text( "//" ), rdescript="Java: Add Comment"),
        "long comment":                     R(Text("/**/")+Key("left,left"), rdescript="Java: Long Comment"),
        #
        "value not":                        R(Text("null"), rdescript="Java: Null"),
        #
        "return":                           R(Text("return "), rdescript="Java: Return"),
        #
        "value true":                       R(Text("true"), rdescript="Java: True"),
        "value false":                      R(Text("false"), rdescript="Java: False"),
        
        
        # Java specific
        
        "it are in":                        R(Text("Arrays.asList(NAME).contains(VALUE)"), rdescript="Java: In"),
        "try states":                       R(Text("try"), rdescript="Java: Try"),
        "arrow":                            R(Text("->"), rdescript="Java: Lambda Arrow"),
        
        "public":                           R(Text("public "), rdescript="Java: Public"),
        "private":                          R(Text("private "), rdescript="Java: Private"),
        "static":                           R(Text("static "), rdescript="Java: Static"),
        "final":                            R(Text("final "), rdescript="Java: Final"),
        "void":                             R(Text("void "), rdescript="Java: Void"),
        
        "cast to double":                   R(Text("(double)()")+Key("left"), rdescript="Java: Cast To Double"),
        "cast to integer":                  R(Text("(int)()")+Key("left"), rdescript="Java: Cast To Integer"),
                
        "new new":                          R(Text("new "), rdescript="Java: New"),
        "integer":                          R(Text("int "), rdescript="Java: Integer"),
        "big integer":                      R(Text("Integer "), rdescript="Java: Big Integer"),
        "double tie":                       R(Text("double "), rdescript="Java: Double"),
        "big double":                       R(Text("Double "), rdescript="Java: Big Double"),
        
        "string":                           R(Text("String "), rdescript="Java: String"),
        "boolean":                          R(Text("boolean "), rdescript="Java: Boolean"),
        "substring":                        R(Text("substring"), rdescript="Java: Substring Method"),
         
        "ternary":                          R(Text("()?:") + Key("left:3"), rdescript="Java: Ternary"),
        "this":                             R(Text("this"), rdescript="Java: This"),
        "array list":                       R(Text("ArrayList"), rdescript="Java: ArrayList"),
       
        "continue":                         R(Text("continue"), rdescript="Java: Continue"),
        "sue iffae":                        R(Text("if ()")+Key("left"), rdescript="Java: Short If"),
        "sue shells":                       R(Text("else")+Key("enter"), rdescript="Java: Short Else"),
        
        "shell iffae":                      R(Text("else if ()")+Key("left"), rdescript="Java: Else If"),
        "throw exception":                  R(Text("throw new Exception()")+Key("left"), rdescript="Java: Throw Exception"),
        
        "character at":                     R(Text("charAt"), rdescript="Java: Character At Method"),
        "is instance of":                   R(Text(" instanceof "), rdescript="Java: Instance Of"),
          
    }

    extras   = []
    defaults = {}
    
    token_set = TokenSet(["abstract", "continue", "for", "new", "switch", "assert",
                 "default", "goto", "package", "synchronized", "boolean",
                 "do", "if", "private", "this", "break", "double",
                 "implements", "protected", "throw", "byte", "else",
                 "import", "public", "throws", "case", "enum",
                 "instanceof", "return", "transient", "catch", "extends",
                 "int", "short", "try", "char", "final", "interface",
                 "static", "void", "class", "finally", "long", "strictfp",
                 "volatile", "const", "float", "native", "super", "while"], 
                         "//", 
                         ["/*", "*/"])





control.nexus().merger.add_global_rule(Java())