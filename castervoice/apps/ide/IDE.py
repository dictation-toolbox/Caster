#
# __author__ = "lexxish"
# __license__ = "LGPL"
# __version__ = "3.0"
#

from enum_custom import MultiValueEnum
from enum import Enum

from Command import Command

# general
expand = "expand [selection] [<n>]"
kraken = "smart kraken"
auto_complete = "auto complete"
generate_code = "jen code"
quick_fix = "quickfix"
auto_complete = "auto complete"
code = "format code"
build = "build"
run = "run"
build_and_run = "build and run"
config = "run config"
show_documentation = "show doc"
show_parameters = "show param"

# window navigation
tab = "tee ross|next tab"
prior_tab = "(tee sauce|(prior|previous) tab)"
close_tab = "tee deli [<n>]|close tab [<n>]"
go_to_editor = "go [to] editor"
go_to_project_explorer = "go [to] project"
go_to_terminal = "go [to] term"
new_file = "new file"

# code navigation
go_to_line = "go [to line]"
method_forward = "em ross [<n>]|method forward [<n>]"
method_back = "em sauce [<n>]|method backward [<n>]"
back = "go sauce [<n>]|go back [<n>]"
forward = "go ross [<n>]|go forward [<n>]"
declaration = "go [to] declaration"
usages = "find usages"
symbol = "search symbol"
source = "jump to source"

# find replace
search = "search"
find = "find"
replace = "replace"
find_in_files = "find [in] files"
replace_in_files = "replace [in] files"

# line operations
line_up = "line up [<n>]"
line_down = "line down [<n>]"
delete_line = "delete line"
kill_the_rest_of_line = "kill"
comment_line = "comment line"
uncomment_line = "uncomment line"
duplicate = "duplicate"

# refactor
imports = "optimize imports"
refactor = "refactor"
rename = "rename"
inline = "inline"
extract_method = "extract method"
variable = "extract variable"
field = "extract field"
constant = "extract constant"
extract_param = "extract (param|parameter)"
methods = "implement methods"
override_methods = "override methods"
indent = "auto indent"
format_code = "format [code]"


