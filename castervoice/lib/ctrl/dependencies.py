'''
Created on Oct 7, 2015

@author: synkarius
'''
import os, sys, time, pkg_resources
from pkg_resources import VersionConflict, DistributionNotFound

DARWIN = sys.platform == "darwin"
LINUX = sys.platform == "linux"

def install_type():
    # Checks if Caster install is Classic or PIP.
    try:
        pkg_resources.require("castervoice")
    except VersionConflict:
        pass
    except DistributionNotFound:
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
            pkg_resources.require("{}".format(dep))
        except VersionConflict:
            pass
        except DistributionNotFound:
            missing_list.append('{0}'.format(dep))
    if missing_list:
        pippackages = (' '.join(map(str, missing_list)))
        print("\nCaster: dependencys are missing. Use 'python -m pip install {0}'".format(pippackages))
        time.sleep(10)


def dep_min_version():
    # For classic: Checks for Maintainer specified package requirements.
    # Needs to be manually resolved if Caster requires a specific version of dependency
    # A GitHub Issue URL needed to explain the change to version specific '==' dependency.
    listdependency = ([
        ["dragonfly2", ">=", "0.28.0", "https://github.com/dictation-toolbox/dragonfly/issues/289"],
    ])
    for dep in listdependency:
        package = dep[0]
        operator = dep[1]
        version = dep[2]
        issue_url = dep[3]
        try:
            pkg_resources.require('{0} {1} {2}'.format(package, operator, version))
        except VersionConflict as e:
            if operator == ">=":
                if issue_url is not None:
                    print("\nCaster: Requires {0} v{1} or greater.\nIssue reference: {2}".format(package, version, issue_url))
                print("Update with: 'python -m pip install {} --upgrade' \n".format(package))
            if operator == "==":
                print("\nCaster: Requires an exact version of {0}.\nIssue reference: {1}".format(package, issue_url))
                print("Install with: 'python -m pip install {}' \n".format(e.req))


class DependencyMan:
    # Initializes functions
    def initialize(self):
        install = install_type()
        if install == "classic":
            dep_missing()
            dep_min_version()

    # TODO: Remove variables and underlying logic feature switches based on dependencies. 
    NATLINK = True
    PYWIN32 = True
    WX = True