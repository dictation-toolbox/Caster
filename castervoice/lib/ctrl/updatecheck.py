import os, socket, subprocess
from datetime import datetime, date

from castervoice.lib import settings
from castervoice.lib.ctrl.dependencies import find_pip, install_type
from castervoice.lib import printer

update = None


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
            printer.out("Caster: Internet check failed to resolve CloudFire DNS")
        if e.errno == 10051:  # Unreachable Network
            pass
        if e.errno not in (10051, 11001):  # Unknown Error
            printer.out(e.errno)
        return False


def update_check(command=None):
    
    # Check for updates pip packages castervoice/dragonfly2
    # ToDo: Investigate why adding to com `"python", "-m"` causes erroneous update messages
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
                printer.out("Caster: {0} is up-to-date".format(command.strip('2')))
                update = False
                break
            else:
                printer.out("Caster: Say 'Update {0}' to update.".format(command.strip('2')))
                update = True
                break
    except Exception as e:
        printer.out("Exception from starting subprocess {0}: " "{1}".format(com, e))


def update_timer():
    # Checks for updates every X days on startup
    onlinemode = settings.SETTINGS["online"]["online_mode"]
    lastupdate = settings.SETTINGS["online"]["last_update_date"]
    updateinterval = settings.SETTINGS["online"]["update_interval"]
    if lastupdate == 'None':
        lastupdate = str(date.today())
        settings.SETTINGS["online"]["last_update_date"] = lastupdate
    if onlinemode:
        today = date.today()
        lastdate = datetime.strptime(lastupdate, "%Y-%m-%d").date()
        diff = today - lastdate
        if diff.days >= updateinterval:  # int Days
            if internet_check():
                settings.SETTINGS["online"]["last_update_date"] = str(date.today())
                printer.out("Searching for updates...")
                return True
            else:
                printer.out("\nCaster: Network off-line check network connection\n")
                return False
        else:
            return False
    else:
        printer.out("\nCaster: Off-line mode is enabled\n")
        return False


class UpdateChecker(object):
    # Initializes functions
    def initialize(self):
        install = install_type()
        if update_timer():
            update_check(command="dragonfly2")
            if install is "pip":
                update_check(command="castervoice")
