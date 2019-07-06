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


def findpip():
    # Find the pip.exe script for Python 2.7. Fallback on pip.exe.
    global pip_path
    python_scripts = os.path.join("Python27", "Scripts")
    for path in os.environ["PATH"].split(";"):
        pip = os.path.join(path, "pip.exe")
        if path.endswith(python_scripts) and os.path.isfile(pip):
            pip_path = pip
            break


# Checks if install is Classic or PIP of caster
def installtype():
    try:
        pkg_resources.require("castervoice")
    except VersionConflict:
        pass
    except DistributionNotFound:
        return "classic"
    return "pip"


def internetcheck(host="1.1.1.1", port=53, timeout=3):
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


def DependencyCheck(command=None):
    com = [pip_path, "search", command]
    startupinfo = None
    # print com
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
            if "INSTALLED" and "(latest)":
                print("Caster: {0} is up-to-date".format(command))
                update = False
                break
            else:
                print("Caster: Say 'Update {0}' to update.".format(command))
                update = True
    except Exception as e:
        print("Exception from starting subprocess {0}: " "{1}".format(com, e))


def DepMissing():
    with open('D:\\Backup\\Library\\Documents\\Caster\\requirements.txt') as f:
        requirements = f.read().splitlines()
    for dep in requirements:
        try:
            pkg_resources.require("{}".format(dep))
        except VersionConflict:
            pass
        except DistributionNotFound as e:
            print("\n Caster: A Dependency is missing 'pip install {0}'".format(e.req))
            time.sleep(15)


def DepMinVersion():
    # Dependencies needs to be manually resolved if Caster requires a certain version of dependency
    # Restart Dragon between tests so pkg_resources.require can find packages
    # DepMinVersion Assumes only one package will have "=="
    upgradelist = []
    listdependency = ([
        ["dragonfly2", ">=", "0.13.0", None],
    ])
    for dep in listdependency:
        package = dep[0]
        operator = dep[1]
        version = dep[2]
        url = dep[3]
        try:
            pkg_resources.require('{0} {1} {2}'.format(package, operator, version))
        except VersionConflict as e:
            if operator is ">=":
                upgradelist.append('{0}'.format(package))
            if operator is "==":
                print("\nCaster: Requires an exact version of dependencies")
                print("Install the exact version: 'pip install {0}'".format(e.req))
    if not upgradelist:
        pass
    else:
        pippackages = (' '.join(map(str, upgradelist)))
        print(
            "\nCaster: Requires updated version of dependencies.\n Update With: 'pip install --upgrade {0}' \n"
            .format(pippackages))


class DependencyMan:
    def __init__(self):
        install = installtype()
        findpip()
        if install is "classic":
            DepMinVersion()
            DepMissing()
        if settings.SETTINGS["miscellaneous"]["online_mode"]:
            if internetcheck():
                if install is "pip":
                    DependencyCheck(command="castervoice")
                DependencyCheck(command="dragonfly2")
            else:
                print("\nCaster: Network off-line check network connection\n")
        else:
            print("\nCaster: Off-line mode is enabled\n")
