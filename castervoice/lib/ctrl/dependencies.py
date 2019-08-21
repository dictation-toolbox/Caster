'''
Created on Oct 7, 2015

@author: synkarius
'''
import os, sys, socket, time, pkg_resources, subprocess
from pkg_resources import VersionConflict, DistributionNotFound
from subprocess import Popen

update = None


def find_pip():
    # Find the pip script for Python.
    python_scripts = os.path.join(sys.exec_prefix, "Scripts")
    if sys.platform == "win32":
        pip = os.path.join(python_scripts, "pip.exe")
        return pip
    if sys.platform.startswith("linux"):
        pip = os.path.join(python_scripts, "pip")
        return pip


def install_type():
    # Checks if Caster install is Classic or PIP.
    try:
        pkg_resources.require("castervoice")
    except VersionConflict:
        pass
    except DistributionNotFound:
        return "classic"
    return "pip"


def internet_check(host="1.1.1.1", port=53, timeout=3):
    """
    Checks for network connection via DNS resolution.
    :param host: CloudFire DNS
    :param port: 53/tcp
    :param timeout: An integer
    :return: True or False
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(timeout)
        s.connect((host, port))
        return True
    except socket.error as e:
        if e.errno == 11001:
            print("Caster: Internet check failed to resolve CloudFire DNS")
        if e.errno == 10051:  # Unreachable Network
            pass
        if e.errno not in (10051, 11001):  # Unknown Error
            print(e.errno)
        return False


def dependency_check(command=None):
    # Check for updates pip packages castervoice/dragonfly2
    com = [find_pip(), "search", command]
    startupinfo = None
    global update
    try:
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(com,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             startupinfo=startupinfo)
        out = p.communicate('')
        for line in out:
            if "INSTALLED" and "latest" in line:
                print("Caster: {0} is up-to-date".format(command.strip('2')))
                update = False
                break
            else:
                print("Caster: Say 'Update {0}' to update.".format(command.strip('2')))
                update = True
                break
    except Exception as e:
        print("Exception from starting subprocess {0}: " "{1}".format(com, e))


def dep_missing():
    # Checks for missing dependencies with the classic install
    uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
    requirements = os.path.join(uppath(__file__, 4), "requirements.txt")
    with open(requirements) as f:
        requirements = f.read().splitlines()
    for dep in requirements:
        dep = dep.split("==", 1)[0]
        try:
            pkg_resources.require("{}".format(dep))
        except VersionConflict:
            pass
        except DistributionNotFound as e:
            print(
                "\n Caster: {0} dependency is missing. Use 'pip install {0}' in CMD or Terminal to install"
                .format(e.req))
            time.sleep(15)


def dep_min_version():
    # For classic: Checks for Maintainer specified package requirements.
    # Needs to be manually resolved if Caster requires a specific version of dependency
    # A GitHub Issue URL needed to explain the change to version specific '==' dependency.
    upgradelist = []
    listdependency = ([
        ["dragonfly2", ">=", "0.13.0", None],
    ])
    for dep in listdependency:
        package = dep[0]
        operator = dep[1]
        version = dep[2]
        issueurl = dep[3]
        try:
            pkg_resources.require('{0} {1} {2}'.format(package, operator, version))
        except VersionConflict as e:
            if operator is ">=":
                upgradelist.append('{0}'.format(package))
            if operator is "==":
                print(
                    "\nCaster: Requires an exact version of dependencies. Issue reference: {0} \n"
                    .format(issueurl))
                print("Install the exact version: 'pip install {0}'".format(e.req))
    if not upgradelist:
        pass
    else:
        pippackages = (' '.join(map(str, upgradelist)))
        print(
            "\nCaster: Requires updated version of dependencies.\n Update With: 'pip install --upgrade {0}' \n"
            .format(pippackages))


def online_mode():
    # Tries to import settings on failure online_mode is true
    try:
        from castervoice.lib import settings
        if settings.SETTINGS["miscellaneous"]["online_mode"] is True:
            return True
        else:
            return False
    except ImportError:
        return True


class DependencyMan:
    # Initializes functions
    def initialize(self):
        install = install_type()
        if install is "classic":
            dep_min_version()
            dep_missing()
        if online_mode() == True:
            if internet_check() == True:
                dependency_check(command="dragonfly2")
                if install is "pip":
                    dependency_check(command="castervoice")
            else:
                print("\nCaster: Network off-line check network connection\n")
        else:
            print("\nCaster: Off-line mode is enabled\n")

    NATLINK = True
    PIL = True
    PYWIN32 = True
    WX = True
