# CCR Languages Quick Reference

A quick reference guide for the language-specific commands included with Caster. Use the `"enable <language>"` command to activate a particular module.

Classic Install Location: `castervoice\rules\ccr` in Caster source code.

- [Bash](#bash)
- [C++](#c)
- [C&#35;](#c-1)
- [VoiceDevCommands](#VoiceDevCommands)
- [Haxe](#haxe)
- [HTML](#html)
- [CSS](#css)
- [Java](#java)
- [Javascript](#javascript)
- [LaTeX](#latex)
- [Matlab](#matlab)
- [Markdown](#markdown)
- [Prolog](#prolog)
- [Python](#python)
- [R](#r)
- [Rust](#rust)
- [SQL](#sql)
- [VHDL](#vhdl)

# Bash

| Command     | Output                             | Command          | Output          |
| ----------- | ---------------------------------- | ---------------- | --------------- |
| add comment | `#`                                | lodge and        | `&&`            |
| breaker     | `break`                            | lodge not        | `!`             |
| case of     | `TOKEN) ;;`                        | lodge or         | &#124; &#124;   |
| continue    | `continue`                         | print to console | `echo`          |
| default     | `*) ;;`                            | push             | `TOKEN+=()`     |
| do loop     | `until [ ]; do`                    | return           | `return`        |
| end switch  | `esac`                             | she bang         | `#!/bin/bash`   |
| for each    | `for TOKEN in TOKEN; do`           | shell iffae      | `elif [[ ]];`   |
| for loop    | `for (( i=0; i<=TOKEN; i++ )); do` | shells           | `else`          |
| function    | `TOKEN(){}`                        | sue iffae        | `[[ ]]`         |
| iffae       | `if [[ ]];`                        | switch           | `case TOKEN in` |
| import      | `. /path/to/functions`             | value false      | `false`         |
| key do      | `do`                               | value not        | `-z "$var"`     |
| key done    | `done`                             | value true       | `true`          |
| key fee     | `fi`                               | while loop       | `while [ ]; do` |
| length of   | `${#TOKEN[@]}`                     |                  |                 |

# C++

| Command                     | Output                            | Command             | Output                                     |
| --------------------------- | --------------------------------- | ------------------- | ------------------------------------------ |
| ([global] scope / name)     | `::`                              | integer             | `int`                                      |
| (pointer / D reference)     | `*`                               | lodge and           | `&&`                                       |
| (reference to / address of) | `&`                               | lodge not           | `!`                                        |
| Vic                         | `vector`                          | lodge or            | &#124; &#124;                              |
| add comment                 | `//`                              | long comment        | `/**/`                                     |
| array                       | `Brackets`                        | member              | `->`                                       |
| big integer                 | `Integer`                         | new new             | `new`                                      |
| breaker                     | `break;`                          | print to console    | `cout <<`                                  |
| case of                     | `case :`                          | private             | `private`                                  |
| character                   | `char`                            | public              | `public`                                   |
| class                       | `class TOKEN{}`                   | pushback            | `push_back`                                |
| constant                    | `const`                           | return              | `return`                                   |
| convert to floating point   | `(double)`                        | shells              | `else{}`                                   |
| convert to integer          | `(int)`                           | standard            | `std`                                      |
| convert to string           | `std::to_string()`                | static              | `static`                                   |
| default                     | `default:`                        | static cast double  | `static_cast<double>()`                    |
| do loop                     | `do {}`                           | static cast integer | `static_cast<int>()`                       |
| double                      | `double`                          | string              | `string`                                   |
| final                       | `final`                           | switch              | `switch(){ case : break; default: break;}` |
| for each                    | `for_each (TOKEN, TOKEN, TOKEN);` | ternary             | `()?;`                                     |
| for loop                    | `for (int i=0; i<TOKEN; i++)`     | value false         | `false`                                    |
| function                    | `TOKEN TOKEN(){}`                 | value not           | `null`                                     |
| iffae                       | `if(){}`                          | value true          | `true`                                     |
| import                      | `#include`                        | while loop          | `while ()`                                 |

# C&#35;

| Command                   | Output                          | Command          | Output                                                        |
| ------------------------- | ------------------------------- | ---------------- | ------------------------------------------------------------- |
| (lambda/goes to)          | `=>`                            | internal         | `internal`                                                    |
| add comment               | `//`                            | list             | `List<>`                                                      |
| array                     | `Brackets`                      | lodge and        | `&&`                                                          |
| big integer               | `Integer`                       | lodge not        | `!`                                                           |
| breaker                   | `break;`                        | lodge or         | &#124; &#124;                                                 |
| case of                   | `case :`                        | long comment     | `/**/`                                                        |
| cast double               | `(double)`                      | new new          | `new`                                                         |
| cast integer              | `(int)`                         | print to console | `Console.WriteLine()`                                         |
| character                 | `char`                          | private          | `private`                                                     |
| class                     | `class TOKEN{}`                 | public           | `public`                                                      |
| constant                  | `const`                         | return           | `return`                                                      |
| convert to floating point | `Convert.ToDouble()`            | shells           | `else{`<br/>`}`                                               |
| convert to integer        | `Convert.ToInt32()`             | static           | `static`                                                      |
| convert to string         | `Convert.ToString()`            | string           | `string`                                                      |
| default                   | `default:`                      | struct           | `struct TOKEN {}`                                             |
| do loop                   | `do {`<br/>`}`                  | switch           | `switch(){`<br/>`case : break;`<br/>`default: break;`<br/>`}` |
| double                    | `double`                        | ternary          | `()?t:f`                                                      |
| enum                      | `enum TOKEN {}`                 | using            | `using`                                                       |
| for each                  | `foreach (TOKEN in Collection)` | value false      | `false`                                                       |
| for loop                  | `for (int i=0; i<TOKEN; i++)`   | value not        | `null`                                                        |
| function                  | `TOKEN TOKEN(){}`               | value true       | `true`                                                        |
| iffae                     | `if(){`<br/>`}`                 | var              | `var TOKEN = TOKEN;`                                          |
| integer                   | `int`                           | while loop       | `while ()`                                                    |
| interface                 | `interface TOKEN {}`            |                  |                                                               |

# VoiceDevCommands
| Command                                     | Output                                                                     |
|:--------------------------------------------|:---------------------------------------------------------------------------|
| `dev key`                                   | `Key(""),`                                                                 |
| `dev text`                                  | `Text("")`                                                                 |
| `dev pause`                                 | ` + Pause("")`                                                             |
| `dev function`                              | `Function()`                                                               |
| `dev repeat`                                | ` * Repeat(extra='n')`                                                     |
| `dev choice`                                | `Choice("", {}) `                                                          |
| `dev mouse [<mouse_button>]`                | `Mouse("left")`                                                            |
| `dev mouse current [position]`              | `Mouse("[1003, 537]")`                                                     |
| `dev bring app`                             | `BringApp()`                                                               |
| `dev descript`                              | ` rdescript="MyGrammar: "`                                                 |
| `dev mimic [<text>]`                        | `Mimic("")`                                                                |
| `dev split dictation [<text>]`              | `"this", "is", "an", "example"`                                            |
| `dev execute`                               | `.execute()`                                                               |
| `command [<spec>] key`                      | `"example": Key(""),`                                                      |
| `command [<spec>] key repeat`               | `"example [<n>]": Key("") * Repeat(extra="n"),`                            |
| `command [<spec>] text`                     | `"example": Text(""),`                                                     |
| `command [<spec>] [bring] app`              | `"example": BringApp(),`                                                   |
| `command [<spec>] function`                 | `"example": Function()`                                                    |
| `command [<spec>] mimic [<text>]`           | `"example": Mimic("test"),`                                                |
| `command [<spec>] playback [<text>]`        | `"example": Playback([(["test", "command"], 0.0),    ,`                    |
| `command [<spec>] mouse [<mouse_button>]`   | `"example": Mouse("[693, 468], left,`                                      |
| `commander [<spec>] key`                    | `"example": R(Key(""), rdescript="MyGrammar: ",`                           |
| `commander [<spec>] key repeat`             | `"example [<n>]": R(Key(""), rdescript="MyGrammar: " * Repeat(extra='n'),` |
| `commander [<spec>] text`                   | `"example": R(Text(""), rdescript="MyGrammar: ",`                          |
| `commander [<spec>] [bring] app`            | `"example": R(BringApp(), rdescript="MyGrammar: ",`                        |
| `commander [<spec>] function`               | `"example": R(Function(), rdescript="MyGrammar: ",`                        |
| `commander [<spec>] mimic [<text>]`         | `"example": R(Mimic("test"), rdescript="MyGrammar: ",`                     |
| `commander [<spec>] mouse [<mouse_button>]` | `"example": R(Mouse("[1244, 690], left, rdescript="" ,`                    |

# Go
| Command                | Output                          |   | Command            | Output                              |
|:-----------------------|:--------------------------------|:--|:-------------------|:------------------------------------|
| iffae                  | `if  {`<br/>` }`                |   | shells             | `else {`<br/>`   }`                 |
| switch                 | `switch  {`<br/>`   }`          |   | case of            | `case :`                            |
| breaker                | `break`                         |   | default            | `default:`                          |
| while loop             | `for  {`<br/>`    }`            |   | for loop           | `for i := 0; i<; i++ {`<br/>`    }` |
| for each               | `for i := range  {`<br/>`    }` |   | convert to integer | `strconv.Atoi()`                    |
| convert to string      | `strconv.Itoa()`                |   | lodge and          | ` && `                              |
| lodge or               | &#124; &#124;                   |   | lodge not          | `!`                                 |
| print to console       | `fmt.Println()`                 |   | import             | `import (`<br/>`)`                  |
| function               | `func `                         |   | class              | `type  struct {`<br/>`   }`         |
| add comment            | `//`                            |   | long comment       | `/**/`                              |
| value not              | `nil`                           |   | return             | `return `                           |
| value true             | `true`                          |   | value false        | `false`                             |
| (inter / integer)      | ``                              |   | boolean            | ``                                  |
| string                 | `string`                        |   | assign             | ` := `                              |
| (function / funk) main | `func main() {`<br/>`    }`     |   | make map           | `make(map[])`                       |
| package                | `package `                      |   |                    | ``                                  |

# Haxe

| Command                   | Output                    | Command          | Output                                                        |
| ------------------------- | ------------------------- | ---------------- | ------------------------------------------------------------- |
| add comment               | `//`                      | integer          | `Int`                                                         |
| anon funk                 | `->`                      | lodge and        | `&&`                                                          |
| array of                  | `Array<TOKEN>()`          | lodge not        | `!`                                                           |
| boolean                   | `Bool`                    | lodge or         | &#124; &#124;                                                 |
| breaker                   | `break;`                  | long comment     | `/**/`                                                        |
| case of                   | `case :`                  | map of           | `Map<TOKEN, TOKEN>()`                                         |
| class                     | `class`                   | new new          | `new`                                                         |
| convert to floating point | `Std.parseFloat()`        | print to console | `trace()`                                                     |
| convert to integer        | `Std.int()`               | private          | `private`                                                     |
| convert to string         | `Std.string()`            | public           | `public`                                                      |
| default                   | `default:`                | return           | `return`                                                      |
| do loop                   | `do TOKEN while(`<br/>`)` | safe cast        | `cast (TOKEN, TOKEN)`                                         |
| double                    | `Float`                   | shells           | `else`                                                        |
| dynamic                   | `Dynamic`                 | static           | `static`                                                      |
| far / variable            | `var`                     | string           | `String`                                                      |
| for each                  | `for (TOKEN in TOKEN)`    | switch           | `switch(){`<br/>`case : TOKEN;`<br/>`default: TOKEN;`<br/>`}` |
| for loop                  | `for (i in 0...TOKEN)`    | this             | `this`                                                        |
| function                  | `function`                | value false      | `false`                                                       |
| get class                 | `Type.getClass()`         | value not        | `null`                                                        |
| get name                  | `Type.getClassName()`     | value true       | `true`                                                        |
| iffae                     | `if()`                    | void             | `Void`                                                        |
| import                    | `import`                  | while loop       | `while ()`                                                    |
| instance of               | `Std.is()`                |                  |                                                               |

# HTML

| Command                            | Output                         | Command                        | Output                                                          |
| ---------------------------------- | ------------------------------ | ------------------------------ | --------------------------------------------------------------- |
| DOC TYPE                           | `<!DOCTYPE html>`              | list item / LI                 | `<li></li>`                                                     |
| H 1 / heading one                  | `<h1></h1>`                    | main                           | `<main>`<br/>`</main>`                                          |
| H 2 / heading to                   | `<h2></h2>`                    | make link                      | `<a href=''></a>`                                               |
| H 3 / heading three                | `<h3></h3>`                    | map                            | `<map>`<br/>`</map>`                                            |
| H 4 / heading for                  | `<h4></h4>`                    | mark / highlight               | `<mark></mark>`                                                 |
| H 5 / heading five                 | `<h5></h5>`                    | menu                           | `<menu>`                                                        |
| H 6 / heading six                  | `<h6></h6>`                    | menu item                      | `<menuitem>`                                                    |
| H are / HR                         | `<hr>`                         | meta                           | `<meta >`                                                       |
| H group / headings group           | `<hgroup></hgroup>`            | meter                          | `<meter >`                                                      |
| HTML                               | `<html>`<br/>`</html>`         | meter close                    | `</meter>`                                                      |
| abbreviation                       | `<abbr></abbr>`                | navigation / navigate          | `<nav></nav>`                                                   |
| address                            | `<address>`<br/>`</address>`   | noscript                       | `<noscript>`<br/>`</noscript>`                                  |
| anchor                             | `<a></a>`                      | object/ embedded object        | `<object >`                                                     |
| area                               | `<area />`                     | opt group                      | `<optgroup>`<br/>`</optgroup>`                                  |
| article                            | `<article >`                   | option                         | `<option >`                                                     |
| audio                              | `<audio>`                      | option close                   | `</option>`                                                     |
| base                               | `<base >`                      | optional break                 | `<option <br>`<br/>`>`                                          |
| body                               | `<body>`<br/>`</body>`         | ordered list / OL              | `<ol>`<br/>`</ol>`                                              |
| bold                               | `<b></b>`                      | output                         | `<output >`                                                     |
| break / be are / BR                | `<br>`                         | output close                   | `</output>`                                                     |
| button                             | `<button></button>`            | override                       | `<bdo></bdo>`                                                   |
| canvas                             | `<canvas >`                    | paragraph                      | `<p>`<br/>`</p>`                                                |
| canvas close                       | `</canvas>`                    | parameter                      | `<param >`                                                      |
| check box                          | `<input type="checkbox">`      | pre format                     | `<pre>`<br/>`</pre>`                                            |
| close article                      | `</article>`                   | progress                       | `<progress >`                                                   |
| close tag                          | `/`                            | quote                          | `<q></q>`                                                       |
| code                               | `<code></code>`                | ruby / pronounce asian         | `<ruby></ruby>`                                                 |
| content                            | `<content>`                    | sample output                  | `<samp></samp>`                                                 |
| data                               | `<data></data>`                | script                         | `<script></script>`                                             |
| data list                          | `<datalist>`<br/>`</datalist>` | section                        | `<section></section>`                                           |
| decorator                          | `<decorator>`                  | select                         | `<select>`<br/>`</select>`                                      |
| defining instance                  | `<dfn></dfn>`                  | semantics / italics            | `<i></i>`                                                       |
| deleted text / deleted / replaced  | `<del></del>`                  | shadow                         | `<shadow>`                                                      |
| description / DD                   | `<dd>`                         | source                         | `<source >`                                                     |
| details                            | `<details>`                    | span                           | `<span></span>`                                                 |
| dialog                             | `<dialog>`                     | strong                         | `<strong></strong>`                                             |
| division                           | `<div></div>`                  | style                          | `<style >`                                                      |
| element                            | `<element>`                    | style close                    | `</style>`                                                      |
| embedded                           | `<embed >`                     | subscript                      | `<sub></sub>`                                                   |
| embraces pronunciation / RT        | `<rt></rt>`                    | summary                        | `<summary>`                                                     |
| emphasis / EM                      | `<em></em>`                    | super script                   | `<sup></sup>`                                                   |
| fall back parenthesis / RP         | `<rp></rp>`                    | table                          | `<table>`                                                       |
| field set                          | `<fieldset>`<br/>`</fieldset>` | table body                     | `<tbody>`                                                       |
| field set close                    | `</fieldset>`                  | table caption / tee caption    | `<caption>`                                                     |
| fig caption                        | `<figcaption>`                 | table cell / TD / tee D        | `<td></td>`                                                     |
| figure                             | `<figure>`                     | table column group / tee group | `<colgroup>`                                                    |
| footer                             | `<footer>`<br/>`</footer>`     | table column / tee column      | `<col>`                                                         |
| form                               | `<form>`<br/>`</form>`         | table foot                     | `<tfoot>`                                                       |
| head                               | `<head>`<br/>`</head>`         | table head / thead             | `<thead>`                                                       |
| header                             | `<header>`<br/>`</header>`     | table header / TH              | `<th>`                                                          |
| image                              | `<img></img>`                  | table macro                    | `<table>`<br/>`<tr>`<br/>`<td></td>`<br/>`</tr>`<br/>`</table>` |
| inline frame                       | `<iframe >`                    | table row / tee are            | `<tr></tr>`                                                     |
| inline frame close                 | `</iframe>`                    | template                       | `<template>`                                                    |
| input                              | `<input >`                     | text area                      | `<textarea >`                                                   |
| inserted text / inserted           | `<ins></ins>`                  | text area close                | `</textarea>`                                                   |
| isolate / bi directional isolation | `<bdi></bdi>`                  | title                          | `<title></title>`                                               |
| keyboard input                     | `<kbd></kbd>`                  | track                          | `<track >`                                                      |
| key gen                            | `<keygen >`                    | underline                      | `<u></u>`                                                       |
| label                              | `<label>`                      | unordered list / UL            | `<ul>`<br/>`</ul>`                                              |
| label close                        | `</label>`                     | variable                       | `<var></var>`                                                   |
| legend                             | `<legend>`                     | video                          | `<video >`                                                      |
| link                               | `<link >`                      | video close                    | `</video>`                                                      |
| list element / DL                  | `<dl>`                         | small                          | `<small></small>`                                               |
| time                               | `<time></time>`                |                                |                                                                 |
# CSS

The CSS commands are designed just like human language. Basically you can write CSS exactly as you read it.
For writing selector, you just dictate as you normally would and then say selector to put brackets
input: dot example selector
output: .example{
}
You can also use pseudo-classes, just say the name.
Input: dot example before selector
output: .example::before{
}

Input: dot example hover selector
output: .example:hover{
}

For writing properties, just say the name of a property to write it And put the cursor where you need to insert value. example:
input: border radius
output: border-radius:;

input: background color
output: background-color:;
you can use any property just like this

For writing units just say the value and unit. for example:
input: 10 pixel
output: 10px
list of units
Pixel or px, percentage or percent, centimeter or cm, inch or in, millimeter or mm, pica or pc, points or pt, ch, em, rem, ex, viewport height or vh, viewport width or vw, millisecond or ms, second or S

# Java

| Command        | Output       | Command            | Output                                                                                                                                                                                  |
| -------------- | ------------ | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| add comment    | `//`         | iterate and remove | `for (Iterator<TOKEN> iterator = TOKEN.iterator();`<br/>`iterator.hasNext();) {`<br/>`String string = iterator.next();`<br/>`if (CONDITION) {`<br/>`iterator.remove();`<br/>`}`<br/>`}` |
| array list     | `ArrayList`  | lodge and          | `&&`                                                                                                                                                                                    |
| arrow          | `->`         | lodge not          | `!`                                                                                                                                                                                     |
| big double     | `Double`     | lodge or           | &#124; &#124;                                                                                                                                                                           |
| big integer    | `Integer`    | long comment       | `/**/`                                                                                                                                                                                  |
| boolean        | `boolean`    | new new            | `new`                                                                                                                                                                                   |
| breaker        | `break;`     | print to console   | `java.lang.System.out.println()`                                                                                                                                                        |
| case of        | `case :`     | private            | `private`                                                                                                                                                                               |
| cast to double | `(double)()` | public             | `public`                                                                                                                                                                                |

# Javascript

| Command                   | Output                        | Command          | Output               |
| ------------------------- | ----------------------------- | ---------------- | -------------------- |
| Let                       | `let`                         | lodge and        | `&&`                 |
| add comment               | `//`                          | lodge not        | `!`                  |
| anon funk                 | `() => {`<br/>`}`             | lodge or         | &#124; &#124;        |
| breaker                   | `break;`                      | long comment     | `/**/`               |
| case of                   | `case :`                      | new new          | `new`                |
| catch                     | `catch(e) {`<br/>`}`          | print to console | `console.log()`      |
| const                     | `const`                       | push             | `push`               |
| continue                  | `continue`                    | return           | `return`             |
| convert to floating point | `parseFloat()`                | self             | `self`               |
| convert to integer        | `parseInt()`                  | shell iffae      | `else if ()`         |
| convert to string         | `""+`                         | shells           | `else {`<br/>`}`     |
| default                   | `default:`                    | switch           | `switch() {`<br/>`}` |
| do loop                   | `do {`<br/>`}`                | this             | `this`               |
| document                  | `document`                    | throw            | `throw`              |
| for each                  | `for (TOKEN in TOKEN)`        | timeout          | `setTimeout()`       |
| for loop                  | `for (var i=0; i<TOKEN; i++)` | timer            | `setInterval()`      |
| function                  | `function TOKEN() {`<br/>`};` | try              | `try {`<br/>`}`      |
| has own property          | `hasOwnProperty()`            | value false      | `false`              |
| iffae                     | `if () {`<br/>`}`             | value not        | `null`               |
| index of                  | `indexOf()`                   | value true       | `true`               |
| inner HTML                | `innerHTML`                   | var              | `var`                |
| instance of               | `instanceof`                  | while loop       | `while ()`           |
| length                    | `length`                      |                  |                      |

# LaTeX

Commands are designed to follow LaTeX syntax as closely as possible, for example `insert document class` produces `\documentclass{}`. See lines 69- of caster/lib/ccr/latex/latex.py for a full list of available inputs.

| Command                      | Output                                            | Command                   | Output      |
| ---------------------------- | ------------------------------------------------- | ------------------------- | ----------- |
| `[use] package [<packages>]` | `\usepackage{<packages>}`                         | insert quote              | \`\`''      |
| `[use] package bib latex`    | `\usepackage[style=authoryear]{biblatex}`         | math fraction             | `\frac{}{}` |
| add comment                  | `%`                                               | subscript                 | `_{}`       |
| `begin <element>`            | `\begin{<element>}` </br> </br> `\end{<element>}` | super script              | `^{}`       |
| `insert <command>`           | `\<command>{}`                                    | `symbol [<big>] <symbol>` | `\<symbol>` |
| `insert <commandnoarg>`      | `\<commandnoarg>`                                 |                           |             |

# Matlab

| Command                   | Output          | Command           | Output        |
| ------------------------- | --------------- | ----------------- | ------------- |
| add comment               | `%`             | lodge not         | `~`           |
| assign                    | `=`             | lodge or          | &#124; &#124; |
| breaker                   | `break`         | long comment      | `%[%]]`       |
| class                     | `classdef`      | print to console  | `disp()`      |
| convert to floating point | `str2num()`     | return            | `return`      |
| convert to integer        | `str2num()`     | section           | `%%`          |
| convert to string         | `num2str()`     | shell iffae / LFA | `elseif`      |
| for each                  | `for m = 1:`    | shells            | `else`        |
| for loop                  | `for`           | sprint F          | `sprintf()`   |
| function                  | `function [] =` | value false       | `false`       |
| iffae                     | `if`            | value not         | `NaN`         |
| import                    | `library()`     | value true        | `true`        |
| length of                 | `length()`      | while loop        | `while`       |
| lodge and                 | `&&`            |                   |               |

# Markdown

| Command                          | Command                  |
|:---------------------------------|:-------------------------|
| `heading [<num>] [<dict>]`       | `table row <n>`          |
| `table (break / split) <n>`      | `insert header`          |
| `insert list`                    | `insert numbered list`   |
| `insert [block] quote`           | `insert link`            |
| `insert image`                   | `insert reference`       |
| `insert equation`                | `insert math`            |
| `insert (italics / italic text)` | `insert bold [text]`     |
| `insert strike through [text]`   | `insert horizontal rule` |
| `insert R code`                  | `insert in line code`    |
| `insert code [block]`            | ` `                      |


# Prolog

| Command             | Output               | Command | Output   |
| ------------------- | -------------------- | ------- | -------- |
| Anonymous           | `_`                  | Rule    | `() :-.` |
| Close Block comment | `*\`                 | comment | `%`      |
| Fail                | `Fail`               | cut     | `!`      |
| Not                 | `\+`                 | iffae   | `( ; )`  |
| Open Block comment  | `/*`                 | implies | `:-`     |
| Or                  | `;`                  |         |          |

# Python

| Command                   | Output                        | Command           | Output                        |
| ------------------------- | ----------------------------- | ----------------- | ----------------------------- |
| [dot] (pie / pi)          | `.py`                         | lodge not         | `!`                           |
| add comment               | `#`                           | lodge or          | `or`                          |
| breaker                   | `break`                       | long comment      | `''''''`                      |
| class                     | `class`                       | long not          | `not`                         |
| convert to character      | `chr()`                       | make assertion    | `assert`                      |
| convert to floating point | `float()`                     | open file         | `open('filename', 'r') as f:` |
| convert to integer        | `int()`                       | print to console  | `print()`                     |
| convert to string         | `str()`                       | read lines        | `content = f.readlines()`     |
| for each                  | `for in :`                    | return            | `return`                      |
| for loop                  | `for i in range(0, ):`        | self              | `self`                        |
| from                      | `from`                        | shell iffae / LFA | `elif :`                      |
| function                  | `def`                         | shells            | `else:`                       |
| global                    | `global`                      | sue iffae         | `if`                          |
| identity is               | `is`                          | sue shells        | `else`                        |
| iffae                     | `if :`                        | try catch         | `try: except Exception:`      |
| import                    | `import`                      | value false       | `False`                       |
| it are in                 | `in`                          | value not         | `None`                        |
| jason                     | `json`                        | value true        | `True`                        |
| length of                 | `len()`                       | while loop        | `while :`                     |
| list comprehension        | `[x for x in TOKEN if TOKEN]` | with              | `with`                        |
| lodge and                 | `and`                         |                   |                               |

# R

| Command         | Output          | Command              | Output                        |
| --------------- | --------------- | -------------------- | ----------------------------- |
| `<function>`    | `<function>()`  | lodge not            | `!`                           |
| NA              | `NA`            | lodge or             | &#124; &#124;                 |
| add comment     | `#`             | print to console     | `print()`                     |
| assign          | `<-`            | return               | `return()`                    |
| breaker         | `break`         | see as vee           | `csv`                         |
| contained in    | `%in%`          | shells               | `else`                        |
| dot (our/are)   | `.R`            | slurp / chain        | `%>%`                         |
| for each        | `for ( in ):`   | tell (slurp / chain) | `{end of line} %>% {newline}` |
| for loop        | `for (i in 1:)` | tell add             | `{end of line} + {newline}`   |
| function        | `function()`    | tidy verse           | `tidyverse`                   |
| `graph <ggfun>` | `<ggfun>()`     | value false          | `FALSE`                       |
| iffae           | `if ()`         | value not            | `NULL`                        |
| import          | `library()`     | value true           | `TRUE`                        |
| lodge and       | `&&`            | while loop           | `while ()`                    |

## Core/TidyVerse Functions

If you are having trouble with over-recognition (R commands appearing where you don't want them) due to the large number of commands, consider adding a prefix to the `<function>` command - line 93 - in lib/ccr/r/r.py to increase phonetic distinctness.

| Command             | Output               | Command            | Output              |
| ------------------- | -------------------- | ------------------ | ------------------- |
| (LM / linear model) | `lm()`               | library            | `library()`         |
| arrange             | `arrange()`          | list               | `list()`            |
| as character        | `as.character()`     | mean               | `mean()`            |
| as data frame       | `as.data.frame()`    | mutate             | `mutate()`          |
| as double           | `as.double()`        | names              | `names()`           |
| as factor           | `as.factor()`        | paste              | `paste0()`          |
| as numeric          | `as.numeric()`       | read CSV           | `read_csv()`        |
| bind rows           | `bind_rows()`        | rename             | `rename()`          |
| case when           | `case_when()`        | select             | `select()`          |
| count               | `count()`            | starts with        | `starts_with()`     |
| drop NA             | `drop_na()`          | string contains    | `str_contains()`    |
| filter              | `filter()`           | string detect      | `str_detect()`      |
| full join           | `full_join()`        | string replace     | `str_replace()`     |
| gather              | `gather()`           | string replace all | `str_replace_all()` |
| group by            | `group_by()`         | sum                | `sum()`             |
| head                | `head()`             | summarise          | `summarise()`       |
| inner join          | `inner_join()`       | tail               | `tail()`            |
| install packages    | `install.packages()` | trim white space   | `trimws()`          |
| is NA               | `is.na()`            | ungroup            | `ungroup()`         |
| left join           | `left_join()`        | vector             | `c()`               |
| length              | `length()`           |                    |                     |

## Graph Plotting Functions

Should all be prefixed with `graph`

| Command       | Output            | Command          | Output             |
| ------------- | ----------------- | ---------------- | ------------------ |
| path [plot]   | `geom_path()`     | density [plot]   | `geom_density()`   |
| line [plot]   | `geom_line()`     | smooth [plot]    | `geom_smooth()`    |
| column [plot] | `geom_col()`      | histogram [plot] | `geom_histogram()` |
| point [plot]  | `geom_point()`    | ex label         | `xlab()`           |
| save          | `ggsave()`        | ex limit         | `xlim()`           |
| facet grid    | `facet_grid()`    | plot             | `ggplot()`         |
| why label     | `ylab()`          | labels           | `labs()`           |
| theme minimal | `theme_minimal()` |                  |                    |

## Pacman Functions

Should all be prefixed with `pack`

| Command         | Output                | Command     | Output           |
| --------------- | --------------------- | ----------- | ---------------- |
| install version | `p_install_version()` | load        | `p_load()`       |
| nstall          | `p_install()`         | install hub | `p_install_gh()` |
| unload          | `p_unload()`          | update      | `p_update()`     |
| install temp    | `p_temp()`            |             |                  |

# Rust

| Command                                | Output                                   | Command            | Output                                       |
| -------------------------------------- | ---------------------------------------- | -------------------| -------------------------------------------- |
| `[unsigned] integer [<ibits>]`         | `[u32] i32`                              | long comment       | `/// `                                       |
| add comment                            | `// `                                    | macro assertion    | `assert_eq!()`                               |
| `array [of] size <n>`                  | `[TOKEN; 0..1000]`                       | macro debug        | `dbg!(&)`                                    |
| `bind [mute]`                          | `let [mut ]`                             | macro format string| `format!()`                                  |
| boolean                                | `bool`                                   | macro panic        | `panic!()`                                   |
| brace pan                              | ` `                                      | macro vector       | `vec![]`                                     |
| breaker                                | `break;`                                 | name space         | `::`                                         |
| case of                                | ` => `                                   | of type            | `:`                                          |
| class                                  | `+`                                      | print to console   | `println!()`                                 |
| convert to floating point              | `parse::<f64>().unwrap()`                | `refer to [mute]`  | `&[mut ]`                                    |
| convert to integer                     | `parse::<i32>().unwrap()`                | self               | `self`                                       |
| convert to string                      | `to_string()`                            | return             | `return`                                     |
| default                                | `_`                                      | shells             | `else {}`                                    |
| do loop                                | `while {TOKEN;TOKEN}{}`                  | static             | `static`                                     |
| `enumerate for each [<a> <b>]`         | `for (i, j) in TOKEN.enumerate() {}`     | string             | `String`                                     |
| `enumerate for loop [of <a> [in <n>]]` | `for (i, TOKEN) in (0..1).enumerate(){}` | switch             | `match `                                     |
| `float [<fbits>]`                      | `f32`                                    | ternary            | `if TOKEN == TOKEN { TOKEN } else { TOKEN }` |
| for each                               | `for TOKEN in TOKEN {}`                  | value false        | `false`                                      |
| `for loop [of <a> [in <n>]]`           | `for i in 0..1 {}`                       | value not          | `None`                                       |
| `function [<return>]`                  | `fn TOKEN(TOKEN) [-> TOKEN {}]`          | value some         | `Some()`                                     |
| iffae                                  | `if {}`                                  | value true         | `true`                                       |
| import                                 | `use`                                    | unwrap             | `.unwrap()`                                  |
| infinite loop                          | `loop {}`                                | while loop         | `while TOKEN {}`                             |
| lifetime                               | `''`                                     |                    |                                              |
| lodge and                              | ` && `                                   |                    |                                              |
| lodge not                              | `!`                                      |                    |                                              |
| lodge or                               | ` &#124; &#124; `                        |                    |                                              |

# SQL

| Command           | Output        | Command                   | Output                 |
| ----------------- | ------------- | ------------------------- | ---------------------- |
| alias as          | `AS`          | it are in                 | `IN`                   |
| ascending         | `ASC`         | join                      | `JOIN`                 |
| between           | `BETWEEN`     | left join                 | `LEFT JOIN`            |
| delete            | `DELETE`      | like                      | `LIKE '%'`             |
| descending        | `DESC`        | lodge and                 | `AND`                  |
| equals / equal to | `=`           | lodge or                  | `OR`                   |
| from              | `FROM`        | not equals / not equal to | `<>`                   |
| full join         | `FULL JOIN`   | on columns                | `ON`                   |
| fun average       | `AVG()`       | order by                  | `ORDER BY`             |
| fun count         | `COUNT()`     | over partition by         | `OVER (PARTITION BY )` |
| fun max           | `MAX()`       | right join                | `RIGHT JOIN`           |
| fun min           | `MIN()`       | select                    | `SELECT`               |
| group by          | `GROUP BY`    | select (all / every)      | `SELECT *`             |
| inner join        | `INNER JOIN`  | union                     | `UNION`                |
| insert into       | `INSERT INTO` | update                    | `UPDATE TOKEN SET`     |
| is not null       | `IS NOT NULL` | using                     | `USING ()`             |
| is null           | `IS NULL`     | where                     | `WHERE`                |

# VHDL

| Command                     | Output                                                                  | Command                       | Output                                                                                    |
| --------------------------- | ----------------------------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------- |
| Architecture                | `architecture TOKEN is`<br/>`begin`<br/>`TOKEN`<br/>`end architecture;` | conditional component         | `TOKEN:`<br/>`if () GENERATE TOKEN : TOKEN port mapping ();end generate TOKEN;`           |
| Assignment                  | `<=`                                                                    | convert to integer            | `to_integer()`                                                                            |
| Association                 | `=>`                                                                    | converts to integer specific  | `conv_integer(,)`                                                                         |
| Concatenate                 | `&`                                                                     | converts to signed            | `signed()`                                                                                |
| Down To                     | `downto`                                                                | converts to unsigned specific | `conv_unsigned(,)`                                                                        |
| Input                       | `in`                                                                    | entity                        | `entity TOKEN is`<br/>`port (TOKEN: in std_logic;`<br/>`);`<br/>`end entity;`             |
| Not Equal                   | `/=`                                                                    | for loop                      | `for in to loop`                                                                          |
| Output                      | `out`                                                                   | generate                      | `GENERATE`                                                                                |
| Signal                      | `signal :`                                                              | generate components           | `TOKEN:`<br/>`for TOKEN in to GENERATE TOKEN : TOKEN port mapping ();end generate TOKEN;` |
| Standard Logic              | `std_logic`                                                             | iffae                         | `if () then end if;`                                                                      |
| Standard Logic Vector       | `std_logic_vector`                                                      | integer                       | `integer TOKEN to TOKEN`                                                                  |
| Up To                       | `upto`                                                                  | length                        | `length'`                                                                                 |
| X NOR                       | `xnor`                                                                  | lodge not                     | `not`                                                                                     |
| XOR                         | `xor`                                                                   | lodge or                      | `or`                                                                                      |
| add comment                 | `--`                                                                    | not and                       | `nand`                                                                                    |
| alternate                   | `elsif TOKEN then`                                                      | process                       | `TOKEN: process()`<br/>`begin`<br/>`TOKEN`<br/>`end process;`                             |
| `binary [<amount>] <digit>` | `01`                                                                    | shells                        | `else`                                                                                    |
| case of                     | `case TOKEN is`                                                         | switch                        | `case TOKEN is`<br/>`when 'TOKEN' => TOKEN`<br/>`end case;`                               |
| type                        | `type :`                                                                | when                          | `when`                                                                                    |

# VHDL Components

| Command               | Output                                                                              |
| --------------------- | ----------------------------------------------------------------------------------- |
| component             | `TOKEN: TOKEN`<br/>`(`<br/>`port map(`<br/>`TOKEN <= TOKEN,`<br/><br/>`)`<br/>`);`  |
| component declaration | `component TOKEN is`<br/>`port (TOKEN: in std_logic;`<br/>`);`<br/>`end component;` |
| component declaration | `component TOKEN is`<br/>`port (TOKEN: in std_logic;`<br/>`);`<br/>`end component;` |
