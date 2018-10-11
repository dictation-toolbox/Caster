# CCR languages quick reference

A quick reference guide for the language-specific commands included with Caster. Use the `"enable <language>" ` command to activate a particular module.

* [Bash](#bash)
* [C++](#c)
* [C&#35;](#c-1)
* [Haxe](#haxe)
* [HTML](#html)
* [Java](#java)
* [Javascript](#javascript)
* [LaTeX](#latex)
* [Matlab](#matlab)
* [Prolog](#prolog)
* [Python](#python)
* [R](#r)
* [Rust](#rust)
* [SQL](#sql)
* [VHDL](#vhdl)

# Bash
Command | Output | | Command | Output
---|---|---|---|---
add comment|`# `||lodge and|` && `
breaker|`break`||lodge not|`!`
case of|`TOKEN)  ;;`||lodge or| &#124; &#124;
continue|`continue`||print to console|`echo `
default|`*)  ;;`||push|`TOKEN+=()`
do loop|`until [  ]; do`||return|`return `
end switch|`esac`||she bang|`#!/bin/bash`
for each|`for TOKEN in TOKEN; do`||shell iffae|`elif [[  ]]; `
for loop|`for (( i=0; i<=TOKEN; i++ )); do`||shells|`else`
function|`TOKEN(){}`||sue iffae|`[[  ]]`
iffae|`if [[  ]]; `||switch|`case TOKEN in`
import|`. /path/to/functions`||value false|`false`
key do|`do`||value not|`-z "$var"`
key done|`done`||value true|`true`
key fee|`fi`||while loop|`while [  ]; do`
length of|`${#TOKEN[@]}`|||``


# C++
Command | Output | | Command | Output
---|---|---|---|---
([global] scope / name)|`::`||integer|`int `
(pointer / D reference)|`*`||lodge and|`&&`
(reference to / address of)|`&`||lodge not|`!`
Vic|`vector`||lodge or|&#124; &#124;
add comment|`//`||long comment|`/**/`
array|`Brackets`||member|`->`
big integer|`Integer`||new new|`new `
breaker|`break;`||print to console|`cout <<`
case of|`case :`||private|`private `
character|`char `||public|`public `
class|`class TOKEN{}`||pushback|`push_back`
constant|`const`||return|`return`
convert to floating point|`(double)`||shells|`else{}`
convert to integer|`(int)`||standard|`std`
convert to string|`std::to_string()`||static|`static `
default|`default: `||static cast double|`static_cast<double>()`
do loop|`do {}`||static cast integer|`static_cast<int>()`
double|`double `||string|`string `
final|`final `||switch|`switch(){  case : break;  default: break;}`
for each|`for_each (TOKEN, TOKEN, TOKEN);`||ternary|`()?;`
for loop|`for (int i=0; i<TOKEN; i++)`||value false|`false`
function|`TOKEN TOKEN(){}`||value not|`null`
iffae|`if(){}`||value true|`true`
import|`#include`||while loop|`while ()`


# C&#35;
Command | Output | | Command | Output
---|---|---|---|---
(lambda/goes to)|`=>`||internal|`internal `
add comment|`//`||list|`List<>`
array|`Brackets`||lodge and|`&&`
big integer|`Integer`||lodge not|`!`
breaker|`break;`||lodge or|&#124; &#124;
case of|`case :`||long comment|`/**/`
cast double|`(double)`||new new|`new `
cast integer|`(int)`||print to console|`Console.WriteLine()`
character|`char `||private|`private `
class|`class TOKEN{}`||public|`public `
constant|`const`||return|`return`
convert to floating point|`Convert.ToDouble()`||shells|`else{`<br/>`}`
convert to integer|`Convert.ToInt32()`||static|`static `
convert to string|`Convert.ToString()`||string|`string `
default|`default: `||struct|`struct TOKEN {}`
do loop|`do {`<br/>`}`||switch|`switch(){`<br/>`  case : break;`<br/>`  default: break;`<br/>`  }`
double|`double `||ternary|`()?t:f`
enum|`enum TOKEN {}`||using|`using`
for each|`foreach (TOKEN in Collection)`||value false|`false`
for loop|`for (int i=0; i<TOKEN; i++)`||value not|`null`
function|`TOKEN TOKEN(){}`||value true|`true`
iffae|`if(){`<br/>`  }`||var|`var TOKEN = TOKEN;`
integer|`int `||while loop|`while ()`
interface|`interface TOKEN {}`|||``


# Haxe
Command | Output | | Command | Output
---|---|---|---|---
add comment|`//`||integer|`Int `
anon funk|`->`||lodge and|`&&`
array of|`Array<TOKEN>()`||lodge not|`!`
boolean|`Bool `||lodge or|&#124; &#124;
breaker|`break;`||long comment|`/**/`
case of|`case :`||map of|`Map<TOKEN, TOKEN>()`
class|`class `||new new|`new `
convert to floating point|`Std.parseFloat()`||print to console|`trace()`
convert to integer|`Std.int()`||private|`private `
convert to string|`Std.string()`||public|`public `
default|`default: `||return|`return `
do loop|`do TOKEN while(`<br/>`)`||safe cast|`cast (TOKEN, TOKEN)`
double|`Float `||shells|`else`
dynamic|`Dynamic`||static|`static `
far / variable|`var `||string|`String `
for each|`for (TOKEN in TOKEN)`||switch|`switch(){`<br/>`  case : TOKEN;`<br/>`  default: TOKEN;`<br/>`  }`
for loop|`for (i in 0...TOKEN)`||this|`this`
function|`function `||value false|`false`
get class|`Type.getClass()`||value not|`null`
get name|`Type.getClassName()`||value true|`true`
iffae|`if()`||void|`Void`
import|`import `||while loop|`while ()`
instance of|`Std.is()`|||``


# HTML
Command | Output | | Command | Output
---|---|---|---|---
DOC TYPE|`<!DOCTYPE html>`||list item / LI|`<li></li>`
H 1 / heading one|`<h1></h1>`||main|`<main>`<br/>`</main>`
H 2 / heading to|`<h2></h2>`||make link|`<a href=''></a>`
H 3 / heading three|`<h3></h3>`||map|`<map>`<br/>`</map>`
H 4 / heading for|`<h4></h4>`||mark / highlight|`<mark></mark>`
H 5 / heading five|`<h5></h5>`||menu|`<menu>`
H 6 / heading six|`<h6></h6>`||menu item|`<menuitem>`
H are / HR|`<hr>`||meta|`<meta >`
H group / headings group|`<hgroup></hgroup>`||meter|`<meter >`
HTML|`<html>`<br/>`</html>`||meter close|`</meter>`
abbreviation|`<abbr></abbr>`||navigation / navigate|`<nav></nav>`
address |`<address>`<br/>`</address>`||noscript|`<noscript>`<br/>`</noscript>`
anchor|`<a></a>`||object/ embedded object|`<object >`
area|`<area />`||opt group|`<optgroup>`<br/>`</optgroup>`
article |`<article >`||option|`<option >`
audio|`<audio>`||option close|`</option>`
base|`<base >`||optional break|`<option <br>`<br/>`>`
body|`<body>`<br/>`</body>`||ordered list / OL|`<ol>`<br/>`</ol>`
bold|`<b></b>`||output|`<output >`
break / be are / BR|`<br>`||output close|`</output>`
button|`<button></button>`||override|`<bdo></bdo>`
canvas|`<canvas >`||paragraph|`<p>`<br/>`</p>`
canvas close|`</canvas>`||parameter |`<param >`
checkbox|`<input type="checkbox">`||pre-format|`<pre>`<br/>`</pre>`
close article|`</article>`||progress|`<progress >`
close tag|`/`||quote|`<q></q>`
code|`<code></code>`||ruby / pronounce asian|`<ruby></ruby>`
content|`<content>`||sample output|`<samp></samp>`
data|`<data></data>`||script|`<script></script>`
data list|`<datalist>`<br/>`</datalist>`||section|`<section></section>`
decorator|`<decorator>`||select|`<select>`<br/>`</select>`
defining instance|`<dfn></dfn>`||semantics / italics|`<i></i>`
deleted text / deleted / replaced|`<del></del>`||shadow|`<shadow>`
``|``||small|`<small></small>`
description / DD|`<dd>`||source|`<source >`
details|`<details>`||span|`<span></span>`
dialog|`<dialog>`||strong|`<strong></strong>`
division|`<div></div>`||style|`<style >`
element|`<element>`||style close|`</style>`
embedded|`<embed >`||subscript|`<sub></sub>`
embraces pronunciation / RT|`<rt></rt>`||summary|`<summary>`
emphasis / EM|`<em></em>`||superscript|`<sup></sup>`
fall-back parenthesis / RP|`<rp></rp>`||table|`<table>`
field set|`<fieldset>`<br/>`</fieldset>`||table body|`<tbody>`
field set close|`</fieldset>`||table caption / tee caption|`<caption>`
fig caption|`<figcaption>`||table cell / TD / tee D|`<td></td>`
figure|`<figure>`||table column group / tee group|`<colgroup>`
footer|`<footer>`<br/>`</footer>`||table column / tee column|`<col>`
form|`<form>`<br/>`</form>`||table foot|`<tfoot>`
head|`<head>`<br/>`</head>`||table head / thead|`<thead>`
header|`<header>`<br/>`</header>`||table header / TH|`<th>`
image |`<img></img>`||table macro|`<table>`<br/>`<tr>`<br/>`<td></td>`<br/>`</tr>`<br/>`</table>`
inline frame|`<iframe >`||table row / tee are|`<tr></tr>`
inline frame close|`</iframe>`||template|`<template>`
input|`<input >`||text area|`<textarea >`
inserted text / inserted|`<ins></ins>`||text area close|`</textarea>`
``|``||time|`<time></time>`
isolate / bi-directional isolation|`<bdi></bdi>`||title|`<title></title>`
keyboard input|`<kbd></kbd>`||track|`<track >`
keygen|`<keygen >`||underline|`<u></u>`
label|`<label>`||unordered list / UL|`<ul>`<br/>`</ul>`
label close|`</label>`||variable|`<var></var>`
legend|`<legend>`||video|`<video >`
link|`<link >`||video close|`</video>`
list element / DL|`<dl>`|||``


# Java
Command | Output | | Command | Output
---|---|---|---|---
add comment|`//`||iterate and remove|`for (Iterator<TOKEN> iterator = TOKEN.iterator();`<br/>`iterator.hasNext();) {`<br/>`	String string = iterator.next();`<br/>`if (CONDITION) {`<br/>`iterator.remove();`<br/>`}`<br/>`}`
array list|`ArrayList`||lodge and|` && `
arrow|`->`||lodge not|`!`
big double|`Double `||lodge or| &#124; &#124;
big integer|`Integer `||long comment|`/**/`
boolean|`boolean `||new new|`new `
breaker|`break;`||print to console|`java.lang.System.out.println()`
case of|`case :`||private|`private `
cast to double|`(double)()`||public|`public `
cast to integer|`(int)()`||return|`return `
character at|`charAt`||shell iffae|`else if ()`
class|`class {}`||shells|`else {`<br/>`  }`
continue|`continue`||static|`static `
convert to floating point|`Double.parseDouble()`||string|`String `
convert to integer|`Integer.parseInt()`||string builder|`StringBuilder builder = new StringBuilder();`<br/>`builder.append(orgStr); builder.deleteCharAt(orgStr.length()-1);`
convert to string|`""+`||substring|`substring`
deco override|`@Override`||sue iffae|`if ()`
default|`default: `||sue shells|`elseif`
do loop|`do {`<br/>`  }`||switch|`switch(){`<br/>`  case : break;`<br/>`  default: break;`<br/>`  }`
double tie|`double `||ternary|`()?:`
final|`final `||this|`this`
for each|`for (TOKEN TOKEN : TOKEN)`||throw exception|`throw new Exception()`
for loop|`for (int i=0; i<TOKEN; i++)`||try catch|`try{}catch(Exception e){}`
function|`TOKEN(){}`||try states|`try`
iffae|`if() {`<br/>`  }`||value false|`false`
import|`import `||value not|`null`
integer|`int `||value true|`true`
is instance of|` instanceof `||void|`void `
it are in|`Arrays.asList(TOKEN).contains(TOKEN)`||while loop|`while ()`


# Javascript
Command | Output | | Command | Output
---|---|---|---|---
Let|`let `||lodge and|` && `
add comment|`//`||lodge not|`!`
anon funk|`() => {`<br/>` }`||lodge or| &#124; &#124;
breaker|`break;`||long comment|`/**/`
case of|`case :`||new new|`new `
catch|`catch(e) {`<br/>`  }`||print to console|`console.log()`
const|`const `||push|`push`
continue|`continue`||return|`return `
convert to floating point|`parseFloat()`||self|`self`
convert to integer|`parseInt()`||shell iffae|`else if ()`
convert to string|`""+`||shells|`else {`<br/>`  }`
default|`default: `||switch|`switch() {`<br/>`  }`
do loop|`do {`<br/>`  }`||this|`this`
document|`document`||throw|`throw `
for each|`for (TOKEN in TOKEN)`||timeout|`setTimeout()`
for loop|`for (var i=0; i<TOKEN; i++)`||timer|`setInterval()`
function|`function TOKEN() {`<br/>`  };`||try|`try {`<br/>`  }`
has own property|`hasOwnProperty()`||value false|`false`
iffae|`if () {`<br/>` }`||value not|`null`
index of|`indexOf()`||value true|`true`
inner HTML|`innerHTML`||var|`var `
instance of|`instanceof `||while loop|`while ()`
length|`length`|||``


# LaTeX
Commands are designed to follow LaTeX syntax as closely as possible, for example `insert document class` produces `\documentclass{}`. See lines 69- of caster/lib/ccr/latex/latex.py for a full list of available inputs.

Command | Output | | Command | Output
---|---|---|---|---
`[use] package [<packages>]`|`\usepackage{<packages>}`||insert quote|\`\`''
[use] package bib latex|`\usepackage[style=authoryear]{biblatex}`||math fraction|`\frac{}{} `
add comment|`%`||subscript|`_{}`
`begin <element>`|`\begin{<element>}` </br> </br> `\end{<element>}`||superscript|`^{}`
`insert <command>`|`\<command>{}`||`symbol [<big>] <symbol>`|`\<symbol>`
`insert <commandnoarg>`|`\<commandnoarg>`|||``


# Matlab
Command | Output | | Command | Output
---|---|---|---|---
add comment|`%`||lodge not|`~`
assign|` = `||lodge or| &#124; &#124;
breaker|`break`||long comment|`%[%]]`
class|`classdef `||print to console|`disp()`
convert to floating point|`str2num()`||return|`return `
convert to integer|`str2num()`||section|`%%`
convert to string|`num2str()`||shell iffae / LFA|`elseif `
for each|`for m = 1:`||shells|`else `
for loop|`for `||sprint F|`sprintf()`
function|`function [] = `||value false|`false`
iffae|`if `||value not|`NaN`
import|`library()`||value true|`true`
length of|`length()`||while loop|`while `
lodge and|` && `|||``


# Prolog
Command | Output | | Command | Output
---|---|---|---|---
Anonymous|`_`||Rule|`() :-.`
Close Block comment|`*\ `||comment|`%`
Fail|`Fail`||cut|`!`
Not|`\+`||iffae|`( ;  )`
Open Block comment|`/* `||implies|`:-`
Or|`;`|||``


# Python
Command | Output | | Command | Output
---|---|---|---|---
[dot] (pie / pi)|`.py`||lodge not|`!`
add comment|`#`||lodge or|` or `
breaker|`break`||long comment|`''''''`
class|`class `||long not|` not `
convert to character|`chr()`||make assertion|`assert `
convert to floating point|`float()`||open file|`open('filename', 'r') as f:`
convert to integer|`int()`||print to console|`print()`
convert to string|`str()`||read lines|`content = f.readlines()`
for each|`for  in :`||return|`return `
for loop|`for i in range(0, ):`||self|`self`
from|`from `||shell iffae / LFA|`elif :`
function|`def `||shells|`else:`
global|`global `||sue iffae|`if `
identity is|` is `||sue shells|`else `
iffae|`if :`||try catch|`try: except Exception:`
import|`import `||value false|`False`
it are in|` in `||value not|`None`
jason|`json`||value true|`True`
length of|`len()`||while loop|`while :`
list comprehension|`[x for x in TOKEN if TOKEN]`||with|`with `
lodge and|` and `|||``


# R
Command | Output | | Command | Output
---|---|---|---|---
NA|`NA`||graph smooth [plot]|`geom_smooth()`
add comment|`#`||group by|`group_by()`
arrange|`arrange()`||head of|`head()`
as character|`as.character()`||iffae|`if ()`
as data frame|`as.data.frame()`||import|`library()`
as double|`as.double()`||inner join|`inner_join()`
as factor|`as.factor()`||left join|`left_join()`
as numeric|`as.numeric()`||length of|`length()`
assign|` <- `||library|`library()`
bind rows|`bind_rows()`||list of|`list()`
breaker|`break`||lodge and|` && `
case when|`case_when()`||lodge not|`!`
contained in|` %in% `||lodge or| &#124; &#124;
count|`count()`||mutate|`mutate()`
deeply|`dplyr`||names of|`names()`
dot (our/are)|`.R`||paste of|`paste0()`
filter|`filter()`||print to console|`print()`
for each|`for ( in ):`||rename|`rename()`
for loop|`for (i in 1:)`||return|`return()`
full join|`full_join()`||see as vee|`csv`
function|`function()`||select|`select()`
gather|`gather()`||shell iffae / LFA|`elseif ()`
gee aesthetics|`aes()`||shells|`else `
gee ex label|`xlab()`||slurp / chain|` %>% `
gee ex limit|`xlim()`||summarise|`summarise()`
gee labels|`labs()`||tell (slurp / chain)|`{end of line} %>% {newline}`
gee plot|`ggplot()`||tell add|`{end of line} + {newline}`
gee theme|`theme()`||tidier|`tidyr`
gee title|`ggtitle()`||tidy verse|`tidyverse`
gee why label|`ylab()`||trim white space|`trimws()`
gee why limit|`ylim()`||ungroup|`ungroup()`
graph (scatter / point) [plot]|`geom_point()`||value false|`FALSE`
graph column [plot]|`geom_col()`||value not|`NULL`
graph density [plot]|`geom_density()`||value true|`TRUE`
graph histogram [plot]|`geom_histogram()`||vector of|`c()`
graph line [plot]|`geom_line()`||while loop|`while ()`
graph path [plot]|`geom_path()`|||``


# Rust
Command | Output | | Command | Output
---|---|---|---|---
``[unsigned] integer [<ibits>]``|`[u32] i32 `||lodge and|` && `
add comment|`//`||lodge not|`!`
`array [of] size <n>`|`[TOKEN; 0..1000]`||lodge or|&#124; &#124;
`bind [mute]`|`let [mut ]`||long comment|`///`
boolean|`bool `||macro assertion|`assert_eq!()`
brace pan|``||macro format string|`format!()
breaker|`break;`||macro panic|`panic!()`
case of|` => `||macro vector|`vec![]`
class|`+`||namespace|`::`
convert to floating point|`parse::<f64>().unwrap()`||of type|`: `
convert to integer|`parse::<i32>().unwrap()`||print to console|`println!()`
convert to string|`to_string()`||`refer to [mute]`|`&[mut ]`
default|`_`||return|`return `
do loop|`while {TOKEN;TOKEN}{}`||shells|`else {}`
`enumerate for each [<a> <b>]`|`for (i, j) in TOKEN.enumerate() {}`||static|`static `
`enumerate for loop [of <a> [in <n>]]`|`for (i, TOKEN) in (0..1).enumerate(){}`||string|`String `
`float [<fbits>]`|`f32`||switch|`match`
for each|`for TOKEN in TOKEN {}`||ternary|`if TOKEN == TOKEN { TOKEN } else { TOKEN }`
`for loop [of <a> [in <n>]]`|`for i in 0..1 {}`||value false|`false`
`function [<return>]`|`fn TOKEN(TOKEN) [-> TOKEN {}]`||value not|`None`
iffae|`if  {}`||value some|`Some()`
import|`use `||value true|`true`
infinite loop|`loop {}`||while loop|`while TOKEN {}`
lifetime|`''`|||``


# SQL
Command | Output | | Command | Output
---|---|---|---|---
alias as|` AS `||it are in|` IN `
ascending|` ASC `||join|` JOIN `
between|` BETWEEN `||left join|` LEFT JOIN `
delete|` DELETE `||like|` LIKE '%'`
descending|` DESC `||lodge and |` AND `
equals / equal to|` = `||lodge or|` OR `
from|` FROM `||not equals / not equal to|` <> `
full join|` FULL JOIN `||on columns|` ON `
fun average|` AVG() `||order by|` ORDER BY `
fun count|` COUNT() `||over partition by|` OVER (PARTITION BY ) `
fun max|` MAX() `||right join|` RIGHT JOIN `
fun min|` MIN() `||select|` SELECT `
group by|` GROUP BY `||select (all / every)|` SELECT * `
inner join|` INNER JOIN `||union|` UNION `
insert into|` INSERT INTO `||update|` UPDATE TOKEN SET `
is not null|` IS NOT NULL `||using|` USING () `
is null|` IS NULL `||where|` WHERE `


# VHDL
Command | Output | | Command | Output
---|---|---|---|---
Architecture|`architecture TOKEN is`<br/>`begin`<br/>`  TOKEN`<br/>`end architecture;`||conditional component|`TOKEN:`<br/>`  if ()  GENERATE TOKEN : TOKEN port mapping  ();end generate TOKEN;`
Assignment|` <= `||convert to integer|`to_integer()`
Association|` => `||converts to integer specific|`conv_integer(,)`
Concatenate|` & `||converts to signed|`signed()`
Constant|`constant : `||converts to unsigned|`unsigned()`
Down To|`downto`||converts to unsigned specific|`conv_unsigned(,)`
Input|`in`||entity|`entity TOKEN is `<br/>`  port (TOKEN: in std_logic; `<br/>`    ); `<br/>`  end entity;`
Not Equal|`/=`||for loop|`for  in to loop`
Output|`out`||generate|`GENERATE`
Signal|`signal : `||generate components|`TOKEN:`<br/>`  for TOKEN in  to  GENERATE  TOKEN : TOKEN port mapping  ();end generate TOKEN;`
Standard Logic|`std_logic`||iffae|`if () then end if;`
Standard Logic Vector|`std_logic_vector`||integer|`integer TOKEN to TOKEN`
Up To|`upto`||length|`length'`
X NOR|`xnor`||lodge not|`not`
XOR|`xor`||lodge or|`or`
add comment|`-- `||not and|`nand`
alternate|`elsif TOKEN then`||process|`TOKEN: process()`<br/>`begin`<br/>`  TOKEN`<br/>`end process;`
`binary [<amount>] <digit>`|`01`||shells|`else`
case of|`case TOKEN is`||switch|`case TOKEN is`<br/>`  when 'TOKEN'  =>  TOKEN`<br/>`end case;`
``|``||type|`type :`
component|`TOKEN: TOKEN`<br/>`(`<br/>`    port map(`<br/>`        TOKEN <= TOKEN,`<br/><br/>`)`<br/>`  );`||when|`when `
component declaration|`component TOKEN is`<br/>`  port (TOKEN: in std_logic;`<br/>`    );`<br/>`  end component;`|||``
