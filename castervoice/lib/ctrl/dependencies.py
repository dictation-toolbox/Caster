'''
Created on Oct 7, 2015

@author: synkarius
'''
import os, sys, time
from importlib.metadata import version, PackageNotFoundError
from packaging.version import Version
from castervoice.lib import printer

DARWIN = sys.platform == "darwin"
LINUX = sys.platform == "linux"

def install_type():
    # Checks if Caster install is Classic or PIP.
    try:
        version("castervoice")
    except PackageNotFoundError:
        return "classic"
    return "pip"


def find_pip():
    # Find the pip script for Python.
    python_scripts = os.path.join(sys.exec_prefix,
                                  "bin" if DARWIN or LINUX else "Scripts")
    pip_exec = "pip.exe" if sys.platform == "win32" else "pip"
    return os.path.join(python_scripts, pip_exec)


def dep_missing():
    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    requirements_file = "requirements-mac-linux.txt" if DARWIN or LINUX else "requirements.txt"
    requirements = os.path.join(uppath(__file__, 4), requirements_file)
    missing_list = []
    with open(requirements) as f:
        requirements = f.read().splitlines()
    for dep in requirements:
        dep = dep.split(">=", 1)[0]
        try:
            version(dep)
        except PackageNotFoundError:
            missing_list.append(dep)
    if missing_list:
        pippackages = (' '.join(map(str, missing_list)))
        printer.out("\nCaster: dependencys are missing. Use 'python -m pip install {0}'".format(pippackages))
        time.sleep(10)


def dep_min_version():
    # For classic: Checks for Maintainer specified package requirements.
    # Needs to be manually resolved if Caster requires a specific version of dependency
    # A GitHub Issue URL needed to explain the change to version specific '==' dependency.
    listdependency = ([
        ["dragonfly2", ">=", "0.34.0", "https://github.com/dictation-toolbox/dragonfly/blob/master/CHANGELOG.rst#fixed"],
    ])
    for dep in listdependency:
        package = dep[0]
        operator = dep[1]
        req_version = dep[2]
        issue_url = dep[3]
        try:
            installed = Version(version(package))
            required = Version(req_version)
            if operator == ">=" and installed < required:
                if issue_url is not None:
                    printer.out("\nCaster: Requires {0} v{1} or greater.\nIssue reference: {2}".format(package, req_version, issue_url))
                printer.out("Update with: 'python -m pip install {} --upgrade' \n".format(package))
            elif operator == "==" and installed != required:
                printer.out("\nCaster: Requires an exact version of {0}.\nIssue reference: {1}".format(package, issue_url))
                printer.out("Install with: 'python -m pip install {0}=={1}' \n".format(package, req_version))
        except PackageNotFoundError:
            pass


class DependencyMan:
    # Initializes functions
    def initialize(self):
        install = install_type()
        if install == "classic":
            dep_missing()
            dep_min_version()
