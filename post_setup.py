import os
import urllib2
import logging

logging.basicConfig(format='%(message)s')
log = logging.getLogger()
log.addHandler(logging.FileHandler("caster-install.log", "w"))


def finddirectory():
    try:
        import natlinkstatus
        status = natlinkstatus.NatlinkStatus()
        coredir = status.CoreDirectory
        directory = (os.path.dirname(coredir))
        log.warning("\nCaster: NatLink found.\n" "Defaulting to Dragon NaturallySpeaking Engine\n"
                    "Caster will automatically start with Dragon NaturallySpeaking\n")
        return directory  # NatLink MacroSystem Directory
    except Exception:
        directory = os.path.join(os.environ['USERPROFILE'], "Desktop")
        log.warning("\nCaster: NatLink not found.\n" "Defaulting to Windows Speech Recognition Engine\n"
                    "Click on '_caster' on desktop to launch WSR with Caster\n")
        return directory  # Windows User Desktop Directory


def download():
    try:
        url = 'https://raw.githubusercontent.com/dictation-toolbox/caster/develop/_caster.py'
        response = urllib2.urlopen(url, timeout=10)
        html = response.read()
        directory = finddirectory()
        filename = os.path.join(directory, '_caster.py')
        with open(filename, 'w') as f:
            f.write(html)
    except TypeError as e:
        log.warning('TypeError = ' + str(e))
    except IOError as e:
        log.warning('IOError = ' + str(e))
    except urllib2.HTTPError, e:
        log.warning('HTTPError = ' + str(e.code))
    except Exception:
        import traceback
        log.warning('Generic Exception: ' + traceback.format_exc() + "\nCaster: Report Error to "
                                                                     "https://github.com/dictation-toolbox/caster/issues\n")
def display():
    casterlog = (os.getcwd() + "\caster-install.log")
    log.warning("Close window to continue")
    command = ('type ' + casterlog)
    os.system("start /wait cmd /k " + command)


def main():
    download()
    display()
    pass


if __name__ == '__main__':
    main()
