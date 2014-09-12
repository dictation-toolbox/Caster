from distutils.core import setup
import py2exe,os

setup(	options = {'py2exe': {'bundle_files': 1, "dll_excludes": ["tcl85.dll", "tk85.dll"]}},
		data_files=['C:\\Python27\\tcl\\tcl8.5\\init.tcl'],
		windows=[{"script":"C:\\NatLink\\NatLink\\MacroSystem\\bin\\homebrew\\element\\element_src.py", 'icon_resources':[(1,'icon.ico')]}]
	)