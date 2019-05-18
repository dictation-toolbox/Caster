import os
import shutil
import traceback
import logging

logging.basicConfig(format='%(message)s')
log = logging.getLogger()
log.addHandler(logging.FileHandler("CasterInstall.log", "w"))

supporturl = (
    "\nCaster: Report Error to https://github.com/dictation-toolbox/caster/issues\n")


# On error ensures log file is accessible on desktop to end-user.
# Needed due to temporary directory during PIP install
def copylog():
    directory = os.path.join(os.environ['USERPROFILE'], "Desktop")
    shutil.copy("CasterInstall.log", os.path.join(directory, "CasterInstall.log"))


# Returns directory path for caster and engine "wrs" or "dns"
def finddirectory():
    try:
        import natlinkstatus
        status = natlinkstatus.NatlinkStatus()
        directory = status.getUserDirectory()
        return directory, "dns"  # NatLink MacroSystem Directory
    except ImportError:
        directory = os.path.join(os.environ['USERPROFILE'], "Desktop")
        return directory, "wrs"  # Windows User Desktop Directory


# Copies to directory and renames _caster.py based on engine to caster or UserDirectory directory
def setup():
    directory, engine = finddirectory()
    if os.path.isdir(directory):
        try:
            if engine is "dns":
                shutil.copy("_caster.py", directory)
                log.warning(
                    "\nCaster: NatLink found.\n"
                    "Defaulting to Dragon NaturallySpeaking Engine\n"
                    "Caster will automatically start with Dragon NaturallySpeaking\n")
            if engine is "wrs":
                shutil.copy("_caster.py", os.path.join(directory, "start_caster.py"))
                log.warning(
                    "\nCaster: NatLink not found.\n"
                    "Defaulting to Windows Speech Recognition Engine\n"
                    "Click on 'start_caster.py' on desktop to launch WSR with Caster\n")
        except Exception:
            log.warning('Generic Exception: ' + traceback.format_exc() + supporturl)
            copylog()
    else:
        log.warning("Post install script cannot find directory: " + str(directory) +
                    supporturl)
        copylog()


# Displays CasterInstall.log contents in command prompt window
# Needs to be reimplemented to be OS agnostic.
# Difficult to reimplement do to PIP without reading log file.
def display():
    try:
        casterlog = os.path.join(os.getcwd(), "CasterInstall.log")
        log.warning("Close window to continue")
        command = ("start /wait cmd /k type " + casterlog)
        exitcode = os.system(command)
        if exitcode != 0:
            log.warning("\n An error has occurred to display log file. Exit Code: " +
                        str(exitcode) + supporturl)
            copylog()
    except Exception:
        log.warning('\n An error has occurred to display log file. \n' +
                    traceback.format_exc() + supporturl)
        copylog()


# Kicks off the post install script
def runpostinstall():
    setup()
    display()
