'''
Created on Oct 7, 2015

@author: synkarius
'''

import os, socket, time, pkg_resources, subprocess
from pkg_resources import VersionConflict, DistributionNotFound
from subprocess import Popen
from castervoice.lib import settings

pip_path = None
update = None


def find_pip():
    # Find the pip.exe script for Python 2.7. Fallback on pip.exe.
    global pip_path
    python_scripts = os.path.join("Python27", "Scripts")
    for path in os.environ["PATH"].split(";"):
        pip = os.path.join(path, "pip.exe")
        if path.endswith(python_scripts) and os.path.isfile(pip):
            pip_path = pip
            break


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
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as error:
        print(error.message)
        return False


def dependency_check(command=None):
    # Check for updates pip packages castervoice/dragonfly2
    com = [pip_path, "search", command]
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
    # For classic: Checks for missing dependencies parsing requirements.txt
    base = os.path.normpath(settings.SETTINGS["paths"]["BASE_PATH"] + os.sep + os.pardir)
    requirements = os.path.join(base, "requirements.txt")
    with open(requirements) as f:
        requirements = f.read().splitlines()
    for dep in requirements:
        try:
            pkg_resources.require("{}".format(dep))
        except VersionConflict:
            pass
        except DistributionNotFound as e:
            print("\n Caster: A Dependency is missing 'pip install {0}'".format(e.req))
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


class DependencyMan:
    # Initializes functions
    def __init__(self):
        install = install_type()
        find_pip()
        if install is "classic":
            dep_min_version()
            dep_missing()
        if settings.SETTINGS["miscellaneous"]["online_mode"]:
            if internet_check():
                if install is "pip":
                    dependency_check(command="castervoice")
                dependency_check(command="dragonfly2")
            else:
                print("\nCaster: Network off-line check network connection\n")
        else:
            print("\nCaster: Off-line mode is enabled\n")

    NATLINK = True
    PIL = True
    PYWIN32 = True
    WX = True
